import os
import pandas as pd
import requests
import argparse


def _get_metabolomicsworkbench_filepaths(study_id):

    valid_compression_extensions = [".gz", ".zip", ".7z"]

    try:
        dataset_list_url = "https://www.metabolomicsworkbench.org/data/show_archive_contents_json.php?STUDY_ID={}".format(
            study_id)
        mw_file_list = requests.get(dataset_list_url).json()
        workbench_df = pd.DataFrame(mw_file_list)
    except KeyboardInterrupt:
        raise
    except:
        workbench_df = pd.DataFrame()

    return workbench_df



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Give an MWB study ID and get a dataframe of file paths present in the study.')
    parser.add_argument("--study_id", "-mwb_id", type=str, help='An MWB study ID such as "ST002050", ALL for every study', required=True)
    parser.add_argument("--output_path", type=str, help='The path where the output file should be written. Default is the current working directory.',
                        default=os.getcwd())

    args = parser.parse_args()

    if args.study_id == "ALL":
        # Getting all files
        url = "https://www.metabolomicsworkbench.org/rest/study/study_id/ST/available"
        studies_dict = requests.get(url).json()

        study_list = []
        for key in studies_dict.keys():
            study_dict = studies_dict[key]
            study_list.append(study_dict['study_id'])

        study_list = list(set(study_list))

        all_results_list = []
        for study_id in study_list:
            print("Downloading", study_id)

            try:
                temp_result_df = _get_metabolomicsworkbench_filepaths(study_id=study_id)
                all_results_list.append(temp_result_df)
            except KeyboardInterrupt:
                raise
            except:
                pass

        result_df = pd.concat(all_results_list, axis=0)

    else:
        result_df = _get_metabolomicsworkbench_filepaths(study_id=args.study_id)
    
    output_file = os.path.join(args.output_path, f"{args.study_id}.csv")
    result_df.to_csv(output_file, index=False)

    print(f"Output written to {output_file}")