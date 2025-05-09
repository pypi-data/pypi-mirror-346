import pyTSPA
print(pyTSPA.__version__)
df1 = pyTSPA.load_match_data("C:/Users/henri/Scientific Python/pyTSPA-toolbox/tests/Football_ENG_2017_18.xlsx")
print(df1)
print(pyTSPA.result_stats(df1))