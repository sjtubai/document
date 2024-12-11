import sys
import logging
import os
from datetime import datetime

# Loggerの設定
logging.basicConfig(filename="script_execution.log", level=logging.INFO, format='%(asctime)s [%(levelname)s]: %(message)s')

# テンプレートのプレースホルダーと入力ファイルのインデックスをマッピング
PLACEHOLDER_MAPPING = {
    'A8の位置の値': 8,
    'A10の位置の値': 10,
    'A14の位置の値': 14,
    'A15の位置の値': 15,
    'A20の位置の値': 20,
    'A21の位置の値': 21,
    'A15の位置の値': 15,
}

PLACEHOLDER_RELATED_HOST_MAPPING = {
    "Red": 22,
    "Blue": 23,
    "Yellow": 24,
    "AWSYellow": 25
}

HOST_INFO = {
    "Red": "vmc-osb.hm.jp.honda.com",
    "Blue": "vmc-osb-qa.hm.jp.honda.com",
    "Yellow": "vmc-osb-itb.hm.jp.honda.com",
    "AWSYellow": "vpr-sv-aws101.aws.t.rd.honda.com"
}

def read_template(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        logging.error(f"Error reading template from {file_path}. Error: {e}")
        raise

def generate_output(template, row, host_key):
    for placeholder, index in PLACEHOLDER_MAPPING.items():
        if placeholder in template:
            template = template.replace(placeholder, row[index])
    
    # Add HOST related placeholder
    host_related_index = PLACEHOLDER_RELATED_HOST_MAPPING.get(host_key)
    if host_related_index is not None:
        template = template.replace('A23の位置の値', row[host_related_index])

    host_name = HOST_INFO.get(host_key)
    if host_name:
        template = template.replace('HOST_NAME', host_name)
    
    return template

def main(input_file):
    template_c_path = 'テンプレートファイル_C.txt'
    template_r_path = 'テンプレートファイル_R.txt'
    
    template_c = read_template(template_c_path)
    template_r = read_template(template_r_path)

    # yyyymmddhhmmss形式のタイムスタンプフォルダーの作成
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    root_output_dir = os.path.join(timestamp)
    os.makedirs(root_output_dir, exist_ok=True)
    
    with open(input_file, 'r', encoding='utf-8') as f:
        for line in f:
            # 先頭がタブ文字かどうかを確認
            if line.startswith('\t'):
                # タブ文字で始まる場合、stripとsplitを実行し、先頭に空文字列を挿入
                row = line.strip().split('\t')
                row.insert(0, '')
            else:
                # タブ文字で始まらない場合、通常通りstripとsplitを実行
                row = line.strip().split('\t')
            
            print(row)
            
            for host_key in HOST_INFO.keys():
                try:
                    # Generate output content based on templates
                    output_c = generate_output(template_c, row, host_key)
                    output_r = generate_output(template_r, row, host_key)

                    # 出力ディレクトリの作成
                    output_dir_host = os.path.join(root_output_dir, host_key)
                    os.makedirs(output_dir_host, exist_ok=True)
                    
                    output_dir_c = os.path.join(output_dir_host, 'ContainerAPI')
                    output_dir_r = os.path.join(output_dir_host, 'RewritePath')
                    os.makedirs(output_dir_c, exist_ok=True)
                    os.makedirs(output_dir_r, exist_ok=True)

                    # Write the outputs to respective files
                    with open(os.path.join(output_dir_c, row[58]), 'w', encoding='utf-8') as f_out:
                        f_out.write(output_c)
                    with open(os.path.join(output_dir_r, row[57]), 'w', encoding='utf-8') as f_out:
                        f_out.write(output_r)

                    logging.info(f"Generated files for {host_key} in directories {output_dir_c} and {output_dir_r} successfully.")
                
                except Exception as e:
                    logging.error(f"Error processing row for {host_key}: {row}. Error: {e}")
                    continue

if __name__ == '__main__':
    try:
        if len(sys.argv) != 2:
            logging.error("Incorrect number of arguments provided.")
            print("Usage: python script.py <input_file>")
            sys.exit(1)

        logging.info("start")
        print("start")
        
        input_file = sys.argv[1]
        main(input_file)
        
    except Exception as e:
        logging.error(f"Script execution failed. Error: {e}")
