# mdkit/main.py
import os
import sys
import subprocess
from pathlib import Path
from rich.console import Console
import numpy as np
import periodictable
import math
import readline
from .utils import (
    calculate_molecular_weight,
    calculate_total_mass,
    calculate_box_size
)

class MDKit:
    def __init__(self):
        self.console = Console()
        self.CREATOR_INFO = "[bold blue]Created by Pengcheng Li[/bold blue]"
        
        # 设置自动补全
        readline.set_completer(self.complete_file)
        readline.parse_and_bind("tab: complete")

    def complete_file(self, text, state):
        """自动补全函数，用于补全文件路径"""
        files = [f for f in os.listdir('.') if f.startswith(text)]
        if state < len(files):
            return files[state]
        return None

    def clear_screen(self):
        """清屏（跨平台）"""
        os.system('cls' if sys.platform.startswith('win') else 'clear')

    def main_menu(self):
        """主菜单"""
        self.clear_screen()
        self.console.print(f"[bold cyan]========== MDKIT v0.1 ==========[/bold cyan]")
        self.console.print(self.CREATOR_INFO)
        self.console.print("[bold cyan]===============================[/bold cyan]")
        self.console.print("1) 前处理工具")
        self.console.print("2) 后处理工具")
        self.console.print("0) 退出")
        self.console.print("[bold cyan]===============================[/bold cyan]")
        return input("输入选项: ")

    def preprocess_submenu(self):
        """前处理子菜单"""
        self.clear_screen()
        self.console.print(f"[bold yellow]---- 前处理工具 ----[/bold yellow]")
        self.console.print(self.CREATOR_INFO)
        self.console.print("[bold yellow]---------------------[/bold yellow]")
        self.console.print("1) 构建模拟盒子（Packmol）")
        self.console.print("2) 生成Gromacs的top文件")
        self.console.print("3) 生成Gromacs的预平衡参数（em.mdp）文件")
        self.console.print("4) 生成Gromacs的模拟参数（npt.mdp）文件")
        self.console.print("0) 返回主菜单")
        return input("输入选项: ")

    def run_packmol(self):
        """调用 Packmol 构建模拟盒子"""
        self.console.print("\n[bold]==== 构建模拟盒子（Packmol） ====[/bold]")
        self.console.print(self.CREATOR_INFO)
        self.console.print("[bold]================================[/bold]")
        
        # 输入分子信息
        pdb_files = []
        num_molecules = []
        while True:
            molecule_file = self.console.input("请输入分子或离子的 PDB 文件路径 (如 molecule.pdb，输入 q 结束): ").strip()
            if molecule_file.lower() == 'q':
                break
            if not Path(molecule_file).exists():
                self.console.print(f"[bold red]错误: 文件 {molecule_file} 不存在！[/bold red]")
                continue
            num = int(self.console.input(f"请输入 {molecule_file} 的分子数量: "))
            pdb_files.append(molecule_file)
            num_molecules.append(num)

        if not pdb_files:
            self.console.print("[bold red]错误: 未输入任何分子信息！[/bold red]")
            return

        # 输入目标密度
        target_density = float(self.console.input("请输入目标密度 (g/cm³): "))

        # 计算盒子大小
        box_size = calculate_box_size(pdb_files, num_molecules, target_density)
        box_length = box_size[0]  # 立方体盒子，Lx = Ly = Lz
        self.console.print(f"[bold green]计算得到的盒子大小为: {box_length:.2f} Å x {box_length:.2f} Å x {box_length:.2f} Å[/bold green]")

        # 生成 Packmol 输入文件
        packmol_input = f"tolerance 2.0\nfiletype pdb\n"
        output_file = self.console.input("请输入输出文件路径 (如 output.pdb): ").strip()
        packmol_input += f"output {output_file}\n\n"

        for pdb_file, num in zip(pdb_files, num_molecules):
            packmol_input += f"structure {pdb_file}\n"
            packmol_input += f"    number {num}\n"
            packmol_input += f"    inside box 0. 0. 0. {box_length} {box_length} {box_length}\n"
            packmol_input += "end structure\n\n"

        # 写入 Packmol 输入文件
        input_file = "packmol_input.inp"
        with open(input_file, "w") as f:
            f.write(packmol_input)

        # 调用 Packmol
        try:
            with open(input_file, "r") as f:
                result = subprocess.run(
                    ["packmol"],
                    stdin=f,
                    text=True,
                    capture_output=True
                )
            if result.returncode == 0:
                self.console.print(f"[bold green]模拟盒子构建成功！输出文件: {output_file}[/bold green]")
            else:
                self.console.print(f"[bold red]Packmol 执行失败: {result.stderr}[/bold red]")
        except FileNotFoundError:
            self.console.print("[bold red]错误: 未找到 Packmol 程序，请确保 Packmol 已安装并添加到系统路径中！[/bold red]")
        except subprocess.CalledProcessError as e:
            self.console.print(f"[bold red]Packmol 执行失败: {e.stderr}[/bold red]")
        except Exception as e:
            self.console.print(f"[bold red]未知错误: {str(e)}[/bold red]")

    def generate_gromacs_topology(self, pdb_files, num_molecules):
        """生成 Gromacs 的 top 文件"""
        self.console.print("\n[bold]==== 生成 Gromacs 的 top 文件 ====[/bold]")
        self.console.print(self.CREATOR_INFO)
        self.console.print("[bold]================================[/bold]")
        
        itp_files = []
        for pdb_file in pdb_files:
            molecule_name = Path(pdb_file).stem
            atp_itp_file = f"{molecule_name}_ATP.itp"
            regular_itp_file = f"{molecule_name}.itp"

            if not Path(atp_itp_file).exists():
                self.console.print(f"[bold red]错误: 文件 {atp_itp_file} 不存在！[/bold red]")
                return
            if not Path(regular_itp_file).exists():
                self.console.print(f"[bold red]错误: 文件 {regular_itp_file} 不存在！[/bold red]")
                return

            itp_files.append(atp_itp_file)
            itp_files.append(regular_itp_file)

        top_content = "[ defaults ]\n"
        top_content += "; nbfunc  comb-rule   gen-pairs  fudgeLJ   fudgeQQ\n"
        top_content += "     1        3          yes       0.5       0.5\n\n"

        top_content += "; Include topology\n"
        for itp_file in itp_files:
            if "_ATP.itp" in itp_file:
                top_content += f'#include "{itp_file}"\n'
        for itp_file in itp_files:
            if "_ATP.itp" not in itp_file:
                top_content += f'#include "{itp_file}"\n'
        top_content += "\n"

        system_name = self.console.input("请输入系统名称 (如 Baseline): ").strip()
        top_content += "[ system ]\n"
        top_content += "; Name\n"
        top_content += f"{system_name}\n\n"

        top_content += "[ molecules ]\n"
        top_content += "; Compound     #molecules\n"
        for pdb_file, num in zip(pdb_files, num_molecules):
            molecule_name = Path(pdb_file).stem
            top_content += f"{molecule_name}             {num}\n"

        top_file = self.console.input("请输入输出 top 文件路径 (如 topol.top): ").strip()
        with open(top_file, "w") as f:
            f.write(top_content)

        self.console.print(f"[bold green]Gromacs 的 top 文件生成成功！输出文件: {top_file}[/bold green]")

    def generate_em_mdp(self):
        """生成 Gromacs 的预平衡参数文件（em.mdp）"""
        self.console.print("\n[bold]==== 生成 Gromacs 的预平衡参数文件（em.mdp） ====[/bold]")
        self.console.print(self.CREATOR_INFO)
        self.console.print("[bold]================================[/bold]")
        
        # 从模板文件读取内容
        template_path = os.path.join(os.path.dirname(__file__), 'templates', 'em.mdp.template')
        with open(template_path, 'r') as f:
            em_mdp_content = f.read()

        em_mdp_file = self.console.input("请输入输出 em.mdp 文件路径 (如 em.mdp): ").strip()
        with open(em_mdp_file, "w") as f:
            f.write(em_mdp_content)

        self.console.print(f"[bold green]Gromacs 的预平衡参数文件生成成功！输出文件: {em_mdp_file}[/bold green]")

    def generate_npt_mdp(self):
        """生成 Gromacs 的模拟参数文件（npt.mdp）"""
        self.console.print("\n[bold]==== 生成 Gromacs 的模拟参数文件（npt.mdp） ====[/bold]")
        self.console.print(self.CREATOR_INFO)
        self.console.print("[bold]================================[/bold]")
        
        # 从模板文件读取内容
        template_path = os.path.join(os.path.dirname(__file__), 'templates', 'npt.mdp.template')
        with open(template_path, 'r') as f:
            npt_mdp_content = f.read()

        npt_mdp_file = self.console.input("请输入输出 npt.mdp 文件路径 (如 npt.mdp): ").strip()
        with open(npt_mdp_file, "w") as f:
            f.write(npt_mdp_content)

        self.console.print(f"[bold green]Gromacs 的模拟参数文件生成成功！输出文件: {npt_mdp_file}[/bold green]")

    def handle_main_menu(self, choice):
        """处理主菜单选项"""
        if choice == '1':
            while True:
                sub_choice = self.preprocess_submenu()
                if sub_choice == '0':
                    break
                elif sub_choice == '1':
                    self.run_packmol()
                    input("\n按 Enter 键返回菜单...")
                elif sub_choice == '2':
                    pdb_files = []
                    num_molecules = []
                    while True:
                        molecule_file = self.console.input("请输入分子或离子的 PDB 文件路径 (如 molecule.pdb，输入 q 结束): ").strip()
                        if molecule_file.lower() == 'q':
                            break
                        if not Path(molecule_file).exists():
                            self.console.print(f"[bold red]错误: 文件 {molecule_file} 不存在！[/bold red]")
                            continue
                        num = int(self.console.input(f"请输入 {molecule_file} 的分子数量: "))
                        pdb_files.append(molecule_file)
                        num_molecules.append(num)
                    if not pdb_files:
                        self.console.print("[bold red]错误: 未输入任何分子信息！[/bold red]")
                        continue
                    self.generate_gromacs_topology(pdb_files, num_molecules)
                    input("\n按 Enter 键返回菜单...")
                elif sub_choice == '3':
                    self.generate_em_mdp()
                    input("\n按 Enter 键返回菜单...")
                elif sub_choice == '4':
                    self.generate_npt_mdp()
                    input("\n按 Enter 键返回菜单...")
                else:
                    self.console.print("[bold red]错误: 无效选项![/bold red]")
        elif choice == '2':
            self.console.print("[bold]后处理工具待实现...[/bold]")
        elif choice == '0':
            self.console.print("[bold]再见！[/bold]")
            sys.exit()
        else:
            self.console.print("[bold red]错误: 无效选项![/bold red]")

def main():
    mdkit = MDKit()
    while True:
        try:
            user_choice = mdkit.main_menu()
            mdkit.handle_main_menu(user_choice)
        except KeyboardInterrupt:
            mdkit.console.print("\n[bold yellow]已退出程序[/bold yellow]")
            sys.exit()

if __name__ == "__main__":
    main()