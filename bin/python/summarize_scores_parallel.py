import os
import glob
import subprocess
import concurrent.futures

# 入力フォルダのパス
folder_path = './blast.out.all.d'
output_path = './blast.out.all.d/summarized_scores_0425.d'

top_score_path = '/mnt/share/chiba/orth/blasting.homologene.2022-04/top_score_to_human'

# ファイルパスのリストを取得
file_paths = glob.glob(os.path.join(folder_path, '*.out'))

# コマンドの実行関数
def run_command(file_path):
    # bashコマンドを実行
    file_name, file_ext = os.path.splitext(os.path.basename(file_path))
    command = f'./summarize_scores.pl -t {top_score_path} -v {file_path} ./blast.out.13genes > {os.path.join(output_path, file_name)}.scores.txt'
    print(command)
    subprocess.run(['bash', '-c', command])

# マルチスレッドでコマンドを実行
with concurrent.futures.ThreadPoolExecutor() as executor:
    executor.map(run_command, file_paths)
