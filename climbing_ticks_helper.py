import pandas as pd
from sklearn.metrics import classification_report
import matplotlib.pyplot as plt
import seaborn as sns

def lead_style_order():
    return['Onsight/Flash', 'Redpoint', 'Fell/Hung']

def ordinal_mapping(df):
    ''' DF must have a 'Date' column'''
    return [
        {'col': 'Route Type', 'mapping': {'Sport': 0, 'Trad': 1}},
        {'col': 'Date', 'mapping': {date: i for i, date in enumerate(df['Date'].sort_values().unique())}},
        {'col': 'Safety', 'mapping': {'G': 0, 'PG13': 1, 'R': 2, 'X': 3}},
        {'col': 'Lead Style', 'mapping': {'Onsight/Flash': 0, 'Redpoint': 1, 'Fell/Hung': 2}},
        {'col': 'Rating', 'mapping': {
            'Easy 5th': 0,
            '5.0-': 1, '5.0': 2, '5.0+': 3,
            '5.1-': 4, '5.1': 5, '5.1+': 6,
            '5.2-': 7, '5.2': 8, '5.2+': 9,
            '5.3-': 10, '5.3': 11, '5.3+': 12,
            '5.4-': 13, '5.4': 14, '5.4+': 15,
            '5.5-': 16, '5.5': 17, '5.5+': 18,
            '5.6-': 19, '5.6': 20, '5.6+': 21,
            '5.7-': 22, '5.7': 23, '5.7+': 24,
            '5.8-': 25, '5.8': 26, '5.8+': 27,
            '5.9-': 28, '5.9': 29, '5.9+': 30,
            '5.10-': 31, '5.10a': 32, '5.10a/b': 33, '5.10b': 34, '5.10b/c': 35, '5.10': 36, '5.10c': 37, '5.10c/d': 38, '5.10d': 39, '5.10+': 40,
            '5.11-': 41, '5.11a': 42, '5.11a/b': 43, '5.11b': 44, '5.11b/c': 45, '5.11': 46, '5.11c': 47, '5.11c/d': 48, '5.11d': 49, '5.11+': 50,
            '5.12-': 51, '5.12a': 52, '5.12a/b': 53, '5.12b': 54, '5.12b/c': 55, '5.12': 56, '5.12c': 57, '5.12c/d': 58, '5.12d': 59, '5.12+': 60,
            '5.13-': 61, '5.13a': 62, '5.13a/b': 63, '5.13b': 64, '5.13b/c': 65, '5.13': 66, '5.13c': 67, '5.13c/d': 68, '5.13d': 69, '5.13+': 70,
            '5.14-': 71, '5.14a': 72, '5.14a/b': 73, '5.14b': 74, '5.14b/c': 75, '5.14': 76, '5.14c': 77, '5.14c/d': 78, '5.14d': 79, '5.14+': 80,
            '5.15-': 81, '5.15a': 82, '5.15a/b': 83, '5.15b': 84, '5.15b/c': 85, '5.15': 86, '5.15c': 87, '5.15c/d': 88, '5.15d': 89, '5.15+': 90
        }}
    ]


def combine_predictions_with_data(df, predictions_df):
    '''
    Combine predictions with the original data.

    Parameters:
    df (pd.DataFrame): data that has been grouped and pre-processed, but not ordinalized (for easier reading)
    predictions_df (pd.DataFrame): predictions from the model

    Returns:
    pd.DataFrame: the original data with the predictions added
    '''

    # Re-key columns in predictions_df to indicated that they are predictions
    key_mapping = {'Attempts': 'Predicted Attempts', 'Lead Style': 'Predicted Lead Style'}
    predictions_df = predictions_df.rename(columns=key_mapping)
    
    combined_df = df.copy()
    combined_df = pd.concat([combined_df, predictions_df], axis=1)
    
    # map Predicted Lead Style back to string values
    lead_style_mapping = {i: style for i, style in enumerate(lead_style_order())}
    combined_df['Predicted Lead Style'] = combined_df['Predicted Lead Style'].map(lead_style_mapping)
    
    # reorder columns
    return combined_df[['Route', 'RouteID', 'Date', 'Route Type', 'Alpine', 'Safety', 'Avg Stars', 'Pitches', 'Rating', 'Predicted Lead Style', 'Lead Style', 'Predicted Attempts', 'Attempts']]

def combine_proba_predictions_with_data(df, proba_prediction):
    '''
    Combine probability predictions with the original data.

    Parameters:
    df (pd.DataFrame): data that has been grouped and pre-processed, but not ordinalized (for easier reading)
    proba_prediction (np.ndarray): probability predictions from the model

    Returns:
    pd.DataFrame: the original data with the probability predictions added
    '''
    
    combined_df = df.copy()
    
    # Add new columns for Lead Style predictions
    combined_df['OS/F pred'] = proba_prediction[1][:, 0]
    combined_df['RP pred'] = proba_prediction[1][:, 1]
    combined_df['F/H pred'] = proba_prediction[1][:, 2]
    
    # Add new columns for Attempts predictions
    combined_df['1 Attempt pred'] = proba_prediction[0][:, 0]
    combined_df['2 Attempts pred'] = proba_prediction[0][:, 1]
    # sum all values of 3 attempts or more
    combined_df['3+ Attempts pred'] = proba_prediction[0][:, 2:].sum(axis=1)
    
    # reorder columns
    return combined_df[['Route', 'RouteID', 'Date', 'Route Type', 'Alpine', 'Safety', 'Avg Stars', 'Pitches', 'Rating', 
                        'OS/F pred', 'RP pred', 'F/H pred', 'Lead Style',
                        '1 Attempt pred', '2 Attempts pred', '3+ Attempts pred', 'Attempts']]

def print_classification_report(y_test, y_pred_df):
    fig, ax = plt.subplots(1, len(y_test.columns), figsize=(8, 3))
    if len(y_test.columns) == 1:
        ax = [ax]  # Ensure ax is always a list
    for i, resp in enumerate(y_test.columns):
        cr = classification_report(y_test[resp], y_pred_df[resp], zero_division=0, output_dict=True)
        if resp == 'Lead Style':
            cr['Onsight/Flash'] = cr.pop('0')
            cr['Redpoint'] = cr.pop('1')
            cr['Fell/Hung'] = cr.pop('2')
            cr['accuracy'] = cr.pop('accuracy')
        cr.pop('macro avg', None)
        cr.pop('weighted avg', None)
        cr_df = pd.DataFrame(cr).T.round(2)
        cr_df = cr_df.iloc[:, :-1]
        
        sns.heatmap(cr_df, annot=True, cmap='Reds', cbar=False, fmt='.2f', ax=ax[i])
        ax[i].set_title(f"Classification Report for {resp}")
    plt.tight_layout()
    plt.show()

