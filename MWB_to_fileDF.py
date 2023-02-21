import pandas as pd
import requests
import argparse


def _get_metabolomicsworkbench_filepaths(study_id):

    try:
        dataset_list_url = "https://www.metabolomicsworkbench.org/data/show_archive_contents_json.php?STUDY_ID={}".format(
            study_id)
        mw_file_list = requests.get(dataset_list_url).json()
        workbench_df = pd.DataFrame(mw_file_list)
    except:
        workbench_df = pd.DataFrame()
    workbench_df = workbench_df['FILENAME']
    return workbench_df



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Give an MWB study ID and get a dataframe of file paths present in the study.')
    parser.add_argument("--study_id", "-mwb_id", type=str, help='An MWB study ID such as "ST002050"', required=True)

    args = parser.parse_args()

    result = _get_metabolomicsworkbench_filepaths(study_id = args.study_id)

    result