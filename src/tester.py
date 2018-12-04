


from local.main import main
# from keboola import docker


# cfg = docker.Config('/data/')
# params = cfg.get_parameters()
# analysis_type = cfg.get_parameters()["analysis_type"]
# user_api_key = cfg.get_parameters()["#API_key"]



dev_key = "AIzaSyAkzMRVbmggvF1_l5_Z1fn2CVFivT8KwUI"
analysis_type = 'entities'
# analysis_type = 'syntax'
input_file_path = './sample_files/sample_input.csv'
selected_column = 'bar'


main(
    input_file_path=input_file_path,
    seleted_column=selected_column,
    analysis_type=analysis_type,
    api_key=dev_key
)