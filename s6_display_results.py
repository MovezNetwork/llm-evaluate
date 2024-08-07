import pandas as pd
import ipywidgets as widgets
from IPython.display import display, HTML

def get_input_data():
    output_processed_evaluation_folder_path = 'f9_processed_llm_evaluation_data/'
    mistral_noContext = pd.read_csv(output_processed_evaluation_folder_path + 'Evaluation_NoContext_mistral-medium_corrected.csv')
    mistral_context = pd.read_csv(output_processed_evaluation_folder_path + 'Evaluation_Context_mistral-medium_corrected.csv')
    gpt_noContext = pd.read_csv(output_processed_evaluation_folder_path + 'Evaluation_NoContext_gpt-4_corrected.csv')
    gpt_context = pd.read_csv(output_processed_evaluation_folder_path + 'Evaluation_Context_gpt-4_corrected.csv')

    # adding evaluator info
    mistral_noContext['evaluator'] = 'mistral-medium'
    gpt_noContext['evaluator'] = 'gpt-4'
    mistral_context['evaluator'] = 'mistral-medium'
    gpt_context['evaluator'] = 'gpt-4'

    # adding parallel data info
    is_parallel_map = {0: True, 1: True, 2: False, 3: False}
    mistral_noContext['isParallel'] = mistral_noContext['promptID'].map(is_parallel_map)
    gpt_noContext['isParallel'] = gpt_noContext['promptID'].map(is_parallel_map)
    mistral_context['isParallel'] = mistral_context['promptID'].map(is_parallel_map)
    gpt_context['isParallel'] = gpt_context['promptID'].map(is_parallel_map)
    
    df_noContext = pd.concat([gpt_noContext, mistral_noContext], axis=0)
    df_context = pd.concat([gpt_context, mistral_context], axis=0)

    new_names = {'original': 'neutral_sentence','rewritten_sentence': 'tst_sentence_0', 'your_text': 'user_sentence'}
    df_all = pd.concat([df_noContext, df_context], axis=0)
    df_all.rename(columns=new_names, inplace=True)

    return df_all

def display_interactive_dataframe(df,col_display):
    # Create dropdown widgets for each column you want to filter on
    user_dropdown = widgets.Dropdown(options=['All'] + df['user'].unique().tolist(), value = 'All', description='User:')
    promptID_dropdown = widgets.Dropdown(options=['All'] + df['promptID'].unique().tolist(), value = 'All',description='Prompt ID:')
    model_dropdown = widgets.Dropdown(options=['All'] + df['model'].unique().tolist(), value = 'All', description='Model:')
    shots_dropdown = widgets.Dropdown(options=['All'] + df['shots'].unique().tolist(), value = 'All', description='Shots:')
    isParallel_dropdown = widgets.Dropdown(options=['All', True, False], value = 'All', description='Is Parallel:')
    prompting_dropdown = widgets.Dropdown(options=['All'] + df['prompting'].unique().tolist(), value = 'All', description='Prompting:')
    evaluator_dropdown = widgets.Dropdown(options=['All'] + df['evaluator'].unique().tolist(), value = 'All', description='Evaluator:')
    score_dropdown = widgets.Dropdown(options=['None', 'Accuracy', 'Content_Preservation', 'Fluency'], description='Score:')

    # Create function to update displayed data based on dropdown selections
    def update_data(user, promptID, model, shots, prompting, evaluator, isParallel, score_type):
        filtered_df = df.copy()
        if user != 'All':
            filtered_df = filtered_df[filtered_df['user'] == user]
        if promptID != 'All':
            filtered_df = filtered_df[filtered_df['promptID'] == promptID]
        if model and model != 'All':
            filtered_df = filtered_df[filtered_df['model'] == model]
        if shots != 'All':
            filtered_df = filtered_df[filtered_df['shots'] == shots]
        if prompting != 'All':
            filtered_df = filtered_df[filtered_df['prompting'] == prompting]
        if evaluator != 'All':
            filtered_df = filtered_df[filtered_df['evaluator'] == evaluator]
        if isParallel != 'All':
            filtered_df = filtered_df[filtered_df['isParallel'] == isParallel]

        # Display columns based on score type selection
        if score_type == 'None':
            display_data = filtered_df[col_display]
        elif score_type in ['Accuracy', 'Content_Preservation', 'Fluency']:
            explanation_column = f'explanation_{score_type.lower()}'
            updated_column_list = col_display.copy()
            updated_column_list.append(explanation_column)
            display_data = filtered_df[updated_column_list]
        else:
            print("Invalid score type selected. Displaying original and rewritten_sentence columns only.")
            display_data = filtered_df[col_display]

        # HTML table styling
        html_table = display_data.to_html(index=False)
        styled_html_table = "<style>table {border-collapse: collapse; width: 100%;} th, td {border: 1px solid #dddddd; text-align: left; padding: 8px;} th {background-color: #f2f2f2;} tr:nth-child(even) {background-color: #f2f2f2;}</style>" + html_table

        display(HTML(styled_html_table))


    display(widgets.interactive(update_data, 
                                user=user_dropdown, 
                                promptID=promptID_dropdown, 
                                model=model_dropdown, 
                                shots=shots_dropdown, 
                                prompting=prompting_dropdown, 
                                evaluator=evaluator_dropdown, 
                                isParallel=isParallel_dropdown,
                                score_type=score_dropdown))

        