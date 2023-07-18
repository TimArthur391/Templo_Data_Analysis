import forceplate_data_analyser as fda

txt_file_path = 'scrpts\J-20220927-093421.txt'
            

if txt_file_path:
    data_analyser = fda.ForcePlateDataAnalyser(txt_file_path)

    data_analyser.load_data()

    data_analyser.get_maximum_force_magnitude()