import pandas as pd

def process_data(input):

    temp_df = input.iloc[:, :0]
    temp_df['wickets_remaining'] = 10
    total_wickets = 10
    for (index, ball_num,curr_event) in input[['ball_number', 'current_ball_run']].itertuples():
        if(curr_event==' OUT'):
            total_wickets -= 1
            #Update wicket remaining for the ball and the remaining ones
            temp_df.iloc[index:,:] = total_wickets
            # Update the Out values to 0
            input.iloc[index,4] = 0

    for col in ['ball_number','current_ball_run','chasing_team_won']:
        input[col] = input[col].astype('int8')

    #for each ball add the scores of balls before it
    input['cumulative_runs'] = input['current_ball_run'].cumsum(axis=0)
    input['fraction_of_target'] = input['cumulative_runs'] / input['target']
    input['fraction_of_target'] = input['fraction_of_target'].round(decimals= 3)
    """with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
        print(input['cumulative_runs'])"""

    input['wickets_remaining'] = temp_df
    return input