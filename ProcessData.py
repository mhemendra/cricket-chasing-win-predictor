import pandas as pd

def process_data(input):

    temp_df = input.iloc[:, :0]
    temp_df['wickets_remaining'] = 10
    total_wickets = 10
    for (index, ball_num,curr_event) in input[['ball_number', 'current_ball_run']].itertuples():
        if(curr_event==' OUT'):
            print(index)
            total_wickets -= 1
            temp_df.iloc[index:,:] = total_wickets
            input.iloc[index,4] = 0

    for col in ['ball_number','current_ball_run','chasing_team_won']:
        input[col] = input[col].astype('int8')

    input['cumulative_runs'] = input['current_ball_run'].cumsum(axis=0)

    """with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
        print(input['cumulative_runs'])"""

    input['wickets_remaining'] = temp_df
    #df_with_wickets = pd.concat([input, temp_df], axis=1)
    return input

#with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
    #print(temp_df)
#print(temp_df)
#print(input['ball_number'][:10])

#inp = pd.read_csv(r'data\commentary_data.csv')
#out = process_data(inp)
#out.to_csv(r'data\commentary_data_test.csv', index=None, header=True)
