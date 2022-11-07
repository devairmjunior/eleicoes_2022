"""
Autor: Devair Junior
Criado em: 06/11/2022
Linkedin: https://www.linkedin.com/in/devair-junior

Site do TSE que foi usado como fonte dos datases:
https://dadosabertos.tse.jus.br/dataset/resultados-2022-boletim-de-urna

"""

import requests, zipfile, io, pathlib, os
import pandas as pd


def get_boletim_urna(zip_file_url: str, saving_path: str) -> None:
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:100.0) Gecko/20100101 Firefox/100.0'
        }
        response = requests.get(
            url=zip_file_url,
            headers=headers
        )
        
        extracted_zipfile = zipfile.ZipFile(io.BytesIO(response.content))
        extracted_zipfile.extractall(saving_path)

    except Exception as e:
        raise Exception(f'Erro ao tentar baixar os dados de boletim das urnas. {e}')


def read_boletim_urna(file_path: str) -> pd.DataFrame:
    extracted_list_files = os.listdir(file_path)
    dataset = None
    for file in extracted_list_files:
        if file.endswith('.csv'):
            dataset = file

    if dataset:
        df_boletim_urna = pd.read_csv(os.path.join(file_path, dataset), encoding='latin1', sep=';')
    else:
        raise Exception('Não foi possível encontrar o arquivo csv do dataset')

    return df_boletim_urna


if __name__ == '__main__':
    CURRENT_PATH = pathlib.Path(__file__).parent.resolve()
    saving_path = f'{CURRENT_PATH}/datasets'

    zip_file_url = 'https://cdn.tse.jus.br/estatistica/sead/eleicoes/eleicoes2022/buweb/bweb_2t_PR_311020221535.zip'
    
    print(f'Baixando dados de {zip_file_url}...')
    get_boletim_urna(zip_file_url, saving_path)
    print(f'Dados baixados com sucesso em {CURRENT_PATH}')

    dataset_boletim_urna = read_boletim_urna(file_path=saving_path)

    print(dataset_boletim_urna.head())
