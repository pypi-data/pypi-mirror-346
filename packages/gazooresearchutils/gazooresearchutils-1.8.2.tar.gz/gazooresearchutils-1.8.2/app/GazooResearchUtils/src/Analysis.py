import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from lifelines import KaplanMeierFitter
import matplotlib.pyplot as plt
from typing import List

def pivot(df):
    """
    Pivots the table for easy data analysis using excel.

    inputs:
    df: Dataframe: column names: id, icd10, tag, tag_id, field, data_type, value, phi"
    outputs:
    df: Dataframe: column names are the icd10:tag:field
    """
    df = df.apply(lambda row: pd.Series(data=[row.id,row.tag_id, f"{row.icd10}:{row.tag}:{row.field}", row.value],
                                        index=['mrn','id','name', 'value']),
                                        axis=1)
    df = df.pivot_table(values='value', index=['mrn','id'], columns='name', aggfunc='first') # pivot table
    df = df.droplevel(1) # Remove tag_id
    return df

def multilesion_transforation(data):
    """
    Transforms from patient level analysis to multi-target level analysis

    Parameters:
    data (DataFrame): dataframe from csv data

    Returns:
    df (DataFrame): dataframe from csv data
    """
    # Transformed Dataframe
    df = pd.DataFrame()

    # Unique Targets
    targets = data.loc[data['field'] == 'target-id']
    targets = targets[['id', 'value']]
    targets.columns = ['id', 'target-id']
    targets = targets.drop_duplicates().reset_index()

    # Loop Through Targets
    for index, row in targets.iterrows():
        id = row['id']
        target_id = row['target-id']
        # Select Patients Tags
        pt = data.loc[data['id'] == id]
        # Remove Tags for other targets
        other_target_ids_tag_ids = pt.loc[(pt['field'] == 'target-id') & (pt['value'] != target_id)]['tag_id'].unique().tolist()
        # Filter out Non Target-ids
        pt = pt[~pt['tag_id'].isin(other_target_ids_tag_ids)]
        # Rename id
        pt['id'] = pt['id'].astype(str) + '-' + str(target_id)

        # Concat
        df = pd.concat([df, pt])
    return df

def get_data_dictionary(data):
  """
  Returns data dictionary.

  Parameters:
    data (DataFrame): dataframe with csv data

    Returns:
    dictionary (DataFrame): dataframe with options

  """

  data = data[['icd10', 'tag', 'field', 'data_type']]
  # Remove Duplicates
  dictionary = data.drop_duplicates()
  # Sort
  dictionary = dictionary.sort_values(['icd10', 'tag', 'field'], ascending=[True, True, True])

  return dictionary

def pt_dates_and_events(df, start, event_tags):
  """
  Determines starting date, date of event occurence or data censoring, and whether
  event occured or data was censored

  Parameters:
  df (DataFrame): dataframe for patient
  start (datetime.datetime): datetime
  event_tags (list of dicts): list of possible filters. Structure of filter {'icd10':str, 'tag': str, 'field': str, 'exact': [str, str,...], 'between': [float, float]}
  occurance (int): index of occurance of the start tag

  Returns:
  start (str): date of starting event; None if no starting event
  end (str): earliest date of event occurence or latest known date; None if no
      starting event
  event (int): 1 if event occurred, 0 if data censored; None if no starting event
  """
  # Convert String to Date
  convert_date = lambda date: datetime.strptime(date, '%Y-%m-%d')


  # Get Event Dates
  event_dates = []
  for event_tag in event_tags:
    test = get_tags_where_filter(df, event_tag)
    events = test.loc[((test['field']=='date') | (test['field']=='start-date'))]['value'].to_numpy()
    events = list(map(convert_date, events))
    # Append Dates
    event_dates = event_dates + events

  # Event Dates
  event_dates = np.asarray(event_dates)
  event_dates = np.sort(event_dates)

  # Return Event or Censor
  if len(event_dates) >= 1:
    # Only Keep Event Dates after Start Date
    event_dates = np.where(event_dates > start, event_dates, None)
    event_dates = event_dates[event_dates != np.array(None)]

    # Events
    last = event_dates[-1]
    event = 1
    return start, last, event
  else:
    # Return Censor
    censor_dates = df.loc[(df['field']=='date')].value.to_numpy()
    censor_dates = list(map(convert_date, censor_dates))
    censor_dates = np.sort(censor_dates) # sort
    last = censor_dates[-1]
    event = 0

    return start, last, event

def get_field_value_where_filter(df, filter):
  """
  Get value where filter criteria exists

  Parameters:
  data (DataFrame): dataframe
  filter (dicts): Structure of filter {'icd10':str, 'tag': str, 'field': str, 'exact': [str, str,...], 'between': [float, float]}

  Returns:
  data (DataFrame): dataframe with tags where filter criteria exist

  """

  if "icd10" in filter and "tag" in filter and "field" in filter:
    test = df.loc[(df['icd10'].astype(str) == filter['icd10'])
      & (df['tag'].astype(str) == filter['tag'])
      & (df['field'].astype(str) == filter['field'])]
  elif "tag" in filter and "field" in filter:
    test = df.loc[(df['tag'].astype(str) == filter['tag'])
      & (df['field'].astype(str) == filter['field'])]
  else:
    assert False, f'Filter must have tag, and field'

  return test

def get_tags_where_filter(pt, filter):
  """
  Get tags where filter criteria exists

  Parameters:
  pt (DataFrame): dataframe
  filter (dict): Structure of filter {'icd10':str, 'tag': str, 'field': str, 'exact': [str, str,...], 'between': [float, float]}

  Returns:
  data (DataFrame): dataframe with tags where filter criteria exist

  """
  assert isinstance(pt, pd.DataFrame), f"pt should be a pd.DataFrame, not {type(pt)}"
  assert isinstance(filter, dict), f"filter should be a dict, not {type(filter)}"

  ## Exact ##
  if "exact" in filter and "field" in filter and "tag" in filter and "icd10" in filter:
    test = pt.loc[(pt['icd10'].astype(str) == filter['icd10'])
      & (pt['tag'].astype(str) == filter['tag'])
      & (pt['field'].astype(str) == filter['field'])
      & (pt['value'].isin(filter['exact']))]
    # Get Tags where tag_id
    test = pt.loc[(pt['tag_id'].astype(str).isin(test.tag_id))]
  elif "exact" in filter and "field" in filter and "tag" in filter:
    test = pt.loc[(pt['tag'].astype(str) == filter['tag'])
      & (pt['field'].astype(str) == filter['field'])
      & (pt['value'].isin(filter['exact']))]
    # Get Tags where tag_id
    test = pt.loc[(pt['tag_id'].astype(str).isin(test.tag_id))]
  elif "exact" in filter and "field" in filter :
    test = pt.loc[(pt['field'].astype(str) == filter['field'])
      & (pt['value'].isin(filter['exact']))]
    # Get Tags where tag_id
    test = pt.loc[(pt['tag_id'].astype(str).isin(test.tag_id))]
  ## Between ##
  elif "between" in filter and "field" in filter and "tag" in filter and "icd10" in filter:
    test = pt.loc[(pt['icd10'].astype(str) == filter['icd10'])
      & (pt['tag'].astype(str) == filter['tag'])
      & (pt['field'].astype(str) == filter['field'])]
    # Check Value
    check = pd.to_numeric(test['value']).between(filter['between'][0], filter['between'][1])
    # Get Tags where tag_id
    test = pt.loc[pt['tag_id'].isin(test[check].tag_id)]
  elif "between" in filter and "field" in filter and "tag" in filter:
    test = pt.loc[(pt['tag'].astype(str) == filter['tag'])
      & (pt['field'].astype(str) == filter['field'])]
    # Check Value
    check = pd.to_numeric(test['value']).between(filter['between'][0], filter['between'][1])
    # Get Tags where tag_id
    test = pt.loc[pt['tag_id'].isin(test[check].tag_id)]
  elif "between" in filter and "field" in filter :
    test = pt.loc[(pt['field'].astype(str) == filter['field'])]
    # Check Value
    check = pd.to_numeric(test['value']).between(filter['between'][0], filter['between'][1])
    # Get Tags where tag_id
    test = pt.loc[pt['tag_id'].isin(test[check].tag_id)]
  ## No Field Value Specification ##
  elif "field" in filter and "tag" in filter and "icd10" in filter:
    test = pt.loc[(pt['icd10'].astype(str) == filter['icd10'])
      & (pt['tag'].astype(str) == filter['tag'])
      & (pt['field'].astype(str) == filter['field'])]
    test = pt.loc[(pt['tag_id'].astype(str).isin(test.tag_id))]
  elif "tag" in filter and "icd10" in filter:
    test = pt.loc[(pt['icd10'].astype(str) == filter['icd10'])
      & (pt['tag'].astype(str) == filter['tag'])]
  elif "icd10" in filter:
    test = pt.loc[(pt['icd10'].astype(str) == filter['icd10'])]
  elif "tag" in filter:
    test = pt.loc[(pt['tag'].astype(str) == filter['tag'])]
  elif "field" in filter:
    test = pt.loc[(pt['field'].astype(str) == filter['field'])]
  else:
    test = pd.DataFrame()

  return test

def filter(data, filters, label=''):
  """
  Only include patients that matches all the filter

  Parameters:
  data (DataFrame): dataframe with csv data
  filters (list of dicts): list of possible filters. Structure of filter {'icd10':str, 'tag': str, 'field': str, 'exact': [str, str,...], 'between': [float, float]}
  label (str): label filtered data

  Returns:
  data (DataFrame): dataframe with filters
  """

  df = pd.DataFrame()

  # Loop Through MRNs
  for mrn in data.id.unique():
    #print("mrn",mrn)
    # Select mrn specific Information
    pt = data.loc[(data['id'] == mrn)]

    # Loop Through Conditions
    #print(filters)
    valid = []
    for filter in filters:
      # Get filter
      test = get_tags_where_filter(pt, filter)
      # Is filter apply
      if len(test.index) >= 1: valid.append(True)
      else: valid.append(False)

    # Append mrn to list if all filters apply
    if all(valid):
      df = pd.concat([df, pt])

  # Add Label Column
  df['label'] = label
  return df

def kaplan_meier(data, df_anchors, event_tags):
  """
  Calculate kaplan-meier dataframe.

  Parameters:
  data (DataFrame): dataframe with csv data
  df_anchors (DataFrame): Dataframe of anchors for each patient
  event_tags (list of dicts): list of possible filters. Structure of filter {'icd10':str, 'tag': str, 'field': str, 'exact': [str, str,...], 'between': [float, float]}

  Returns:
  km (DataFrame): dataframe for kaplan meier calculation
  """
  km = pd.DataFrame(columns=['id', 'start-date', 'end-date', 'event'])

  # Loop through patients
  for id in data.id.unique():
    # Patient Data
    pt = data.loc[(data['id'] == id)]

    # Get patient start_date of anchor
    start_date = df_anchors.loc[df_anchors['id'] == id]['value']
    if start_date.empty: continue
    else: start_date = start_date[0]

    # Get Event/Censored
    start, last, event = pt_dates_and_events(pt, start_date, event_tags)

    if not start == None:    # checking if patient has a starting event
      km.loc[len(km)] = [id, start, last, event]

  return km

def time_in_months(start, end):
    """
    Calculate the number of months between start and end dates.

    Parameters:
    start_date (datetime.datetime): starting date in the format YYYY-MM-DD
    end_date (datetime.datetime): end date in the format YYYY-MM-DD

    Returns:
    months (int): number of months (rounded down) between start and end dates
    """
    months = (end.year - start.year) * 12 + end.month - start.month
    if start.day > end.day:
        months -= 1  # round down if not a full month

    return months

def plot_km_curves(km):
    """
    Creates a Kaplan-Meier plot.

    Parameters:
    km (DataFrame): dataframe for kaplan meier
    """

    durations = km.apply(lambda row: time_in_months(row['start-date'], row['end-date']), axis = 1).to_numpy()
    events = km['event'].to_numpy()

    kmf = KaplanMeierFitter()
    kmf.fit(durations, event_observed=events)

    kmf.plot()

    plt.xlabel("Time (months)")
    plt.ylabel("Event Probability")
    plt.title("Kaplan-Meier Curve")
    plt.show()

def get_field_value(data, fields):
  """
  Gets Field Values

  Parameters:
  data (DataFrame): dataframe with csv data
  fields (list of dicts): list of possible fields. Structure of fields {'icd10':str, 'tag': str, 'field': str}

  Returns:
  data (Array): dataframe with columns: id, icd10, tag, field, data_type, value date
  """

  df = pd.DataFrame()

  # Loop Through MRNs
  for mrn in data.id.unique():
    #print("mrn",mrn)
    # Select mrn specific Information
    pt = data.loc[(data['id'] == mrn)]

    # Loop through fields
    for field in fields:
      # Get Field Value
      test_a = pt.loc[(pt['icd10'].astype(str) == field['icd10'])
        & (pt['tag'].astype(str) == field['tag'])
        & (pt['field'].astype(str) == field['field'])]
      test_a = pt.loc[(pt['tag_id'].astype(str).isin(test_a.tag_id))]

      # Loop through tags
      for tag_id in test_a.tag_id.unique():
        test_b = test_a.loc[test_a['tag_id'].astype(str) == tag_id]

        # Get Date
        date = test_b.loc[test_b['data_type'].astype(str) == 'date'].value.tolist()
        if len(date) == 0: date = None
        else: date = date[0]

        # Get Field
        test_b = test_b.loc[test_b['field'].astype(str) == field['field']]

        #
        test_c = test_b[['id','icd10','tag','field','data_type','value']].copy()
        # Add Date Column
        test_c['date'] = date

        # Append Value
        df = pd.concat([df, test_c])

  return df

def line_plot(df, filter, y_scale='day', xlabel="", ylabel=""):
  """
  Creates Line plots across patients. Normalizes it from the 1st instance of the tag.

  inputs:
  df (DataFrame): dataframe with csv data
  filter (dict): Structure of filter {'icd10':str, 'tag': str, 'field': str}
  y_scale (str): Should the y-axis be in years or days.
  xlabel: (str): X-Axis label
  ylabel: (str): Y-Axis label

  outputs:
  df_line_plot (DataFrame): dataframe of line plot data
  """
  assert isinstance(df, pd.DataFrame), f"df should be a pd.DataFrame, not {type(df)}"
  assert isinstance(filter, dict), f"filter should be a dict, not {type(filter)}"
  assert isinstance(y_scale, str), f"y_scale should be a str, not {type(y_scale)}"
  assert y_scale in ['day','year'], f"y_scale should be ['day','year'], not {y_scale}"

  # Extracts tag=psa
  df = get_tags_where_filter(df, filter)

  df_line_plot = pd.DataFrame()
  # Plot Tumor Height
  for patient in df.id.unique():
    df_patient = df.loc[df['id'] == patient]
    df_patient = pivot(df_patient)

    df_patient.reset_index(drop=True, inplace=True) # Remove Index

    # Rename Column to field name. There shouldn't be collisions
    df_patient.columns = [col_name.split(':')[-1] for col_name in df_patient.columns.values]

    # Set Date Field Name
    if 'date' in df_patient.columns: date = 'date'
    elif 'start-date' in df_patient.columns: test = 'start-date'

    df_patient[date] = pd.to_datetime(df_patient[date]) # Convert Date Column to Date Time
    df_patient = df_patient.sort_values(by=date) # Sort by Datetime
    df_patient = df_patient.reset_index(drop=True)
    start_date = df_patient[date][0]
    df_patient['time-delta'] = (df_patient[date] - start_date).dt.days # Calculate DateDiff

    # Convert Time
    if y_scale == 'year': df_patient['time-delta'] = df_patient['time-delta'] / 365.

    # Check to see if field exists.
    if filter['field'] not in df_patient.columns.values: continue

    # Convert to numbers
    values = []
    for value in df_patient[filter['field']].values:
      try:
        value = float(value)
      except:
        value = None
      values.append(value)

    # Plot
    plt.plot(df_patient['time-delta'].values, values, linestyle='-', marker='.')

    # Append
    df_line_plot = pd.concat([df_line_plot, df_patient])

  plt.legend(df.id.unique(), loc='lower right')  # Add Legend
  plt.xlabel(xlabel)
  plt.ylabel("Tumor Height (mm)")
  plt.show()

  return df_line_plot

def get_anchor_dataframe(df, anchors, time_delta, instance):
    """
    Get anchors dataframe for each patient. Order of anchors matters

    inputs:
    df (DataFrame): dataframe with csv data
    time_delta: int: max time in days between anchor
    anchors (list of dicts): list of possible anchors. Structure of anchor {'icd10':str, 'tag': str, 'field': str, 'exact': [str, str,...], 'between': [float, float]}
    instance (int): There may be multiple instances of an anchor. This defines which one matters.

    outputs:
    df_anchors (DataFrame): dataframe of anchors for each patient
    """

    def convertStringToNumber(s, n=8):
        """
        Converts strings to unique numbers. Example ==> 'brachytherapy' -> 96213877
        """
        number = int.from_bytes(s.encode(), 'little')
        return int(str(number)[:n])

    npConvertStringToNumber = np.vectorize(convertStringToNumber)

    def chunker(seq, size):
        return (seq[pos:pos + size] for pos in range(0, len(seq), size))

    def rolling_assessment(data, pattern):
        """Calculates the assessment mean of a NumPy array.
        data: Dataframe
        """
        window_size = len(pattern)

        data['sequence_match'] = False

        if len(data) < window_size:
            print("Window size cannot exceed the data length")
            return data

        for i in range(len(data) - window_size + 1):
            window = data[i:i + window_size]
            if (window['tag'] == pattern).all():
                data.loc[i:i + window_size-1,'sequence_match'] = True
            elif (set(window['tag']) == set(pattern) and window['date_diff'].sum() == timedelta(days=0)):
                data.loc[i:i + window_size-1,'sequence_match'] = True
        return data

    # Get anchors
    df_anchor_tags = pd.DataFrame()
    for anchor in anchors:
        # Get Tags and append
        df_anchor_tags = pd.concat([df_anchor_tags, get_tags_where_filter(df, anchor)])
    df = df_anchor_tags.copy(deep=True)

    # Check if any anchors exist
    df_anchors = pd.DataFrame()
    # Only keep dates values
    df = df.loc[(df['data_type'] == 'date')]
    df = df.loc[(df['field'] == 'date') | (df['field'] == 'start-date')]
    # Loop through patients
    for patient in df['id'].unique():
        # Get Patient Data
        df_patient = df[df['id'] == patient].copy(deep=True)
        # Sort By Dates
        df_patient['value'] = pd.to_datetime(df_patient['value']) # Convert value column to Date Time
        df_patient = df_patient.sort_values(by=['value', 'tag_id']) # Sort by Datetime
        df_patient = df_patient.reset_index(drop=True)

        # Match anchor
        pattern = np.asarray([anchor['tag'] for anchor in anchors])
        df_anchor = pd.DataFrame()
        if len(pattern) >=2:
            # Create Time Diff
            grouping_columns = ['id']
            df_patient['date_diff'] = df_patient.groupby(grouping_columns)['value'].diff()
            # Create tag_number used for rolling
            df_patient = rolling_assessment(df_patient, pattern)
            df_patient = df_patient.drop('date_diff',axis=1)

            # Only keep tags where sequence match is true
            df_patient = df_patient.loc[df_patient['sequence_match']==True]

            # Loop through anchors
            for df_ in chunker(df_patient, len(pattern)):
                df_ = df_.copy(deep=True)
                # Calculate Time Delta
                df_['delta'] = df_['value'].diff()

                if df_['delta'].max() <= timedelta(days=time_delta):
                    df_ = df_.drop(columns=['sequence_match', 'delta'])
                    df_anchor = pd.concat([df_anchor, df_])
        else:
            df_anchor = df_patient

        # Remove Duplicates
        df_anchor = df_anchor.drop_duplicates('tag_id')
        # Break loop if anchor is empty
        if df_anchor.empty: continue

        # Get Tag ID
        tag_id = df_anchor['tag_id'].values[instance]
        df_anchor = df_anchor[df_anchor['tag_id'] == tag_id]

        # Append To Dataframe
        df_anchors = pd.concat([df_anchors, df_anchor])

    return df_anchors

def describe_fields(df, df_anchors, fields, search_range):
  """
  Describes fields around an anchor's start date

  inputs:
  df (DataFrame): dataframe with csv data
  df_anchors (DataFrame): list of anchor tags
  instance (int): There may be multiple instances of an anchor. This defines which one matters.
  search_range: (list[float, float]): Maximum number of days before and after the anchor to search for the field

  outputs:
  df (list[DataFrame]): list of dataframes with field data
  """
  assert isinstance(df, pd.DataFrame), f"df should be a pd.DataFrame, not {type(df)}"
  assert isinstance(df_anchors, pd.DataFrame), f"df_anchors should be a pd.Dataframe, not {type(df_anchors)}"
  assert isinstance(search_range, list), f"search_range should be type list, not {type(time_delta)}"
  for x in search_range: assert isinstance(x, float) or isinstance(s, int), f"range should be a float or int, not {type(x)}"
  assert isinstance(fields, list), f"fields should be type list, not {type(fields)}"
  for field in fields: assert isinstance(field, dict), f"field should be a dict, not {type(field)}"


  df_describe = []
  # Loop through fields
  for idx, field in enumerate(fields):

    df_field_values = pd.DataFrame()
    # Loop through patients
    for patient in df['id'].unique():
      # Get patient specific dataframe
      df_patient = df[df['id'] == patient].copy(deep=True)
      df_anchor = df_anchors[df_anchors['id'] == patient].copy(deep=True)

      # Check if Anchor is Empty
      if df_anchor.empty: continue

      # Get fields
      df_tags = get_tags_where_filter(df_patient, field)
      # Extract Just Dates
      # Only keep dates values
      df_tags = df_tags.loc[df['data_type'] == 'date']
      # Convert value column to Date Time
      df_tags['value'] = pd.to_datetime(df_tags['value'])

      # Check if tags exist
      if df_tags.empty:
        # Add Empty Dataframe
        df_field_values = pd.concat([df_field_values, pd.DataFrame({'id': [patient], 'tag':field['tag'], 'field':field['field'], 'data_type':None, 'value':None})])
        continue

      # Make new column with time delta
      df_tags['delta'] = df_tags.apply(lambda row: (row['value'] - df_anchor['value'][0]).days, axis=1)


      # Check search condition
      df_tags['delta_keep'] = df_tags['delta'].apply(lambda delta: search_range[0] <= delta <= search_range[1])

      # Keep closest row closest
      df_tags['delta'] = df_tags['delta'].apply(lambda delta: abs(delta))
      df_tags = df_tags.sort_values(by=['delta']) # Sort by Datetime

      # Keep rows within time delta
      df_tags = df_tags.loc[df_tags['delta_keep']]

      # Remove Duplicates
      df_tags = df_tags.drop_duplicates()
      tag_ids = df_tags['tag_id'].to_numpy()

      # Get Data For Charts
      df_patient = df_patient.loc[df_patient['tag_id'].astype(str).isin(tag_ids)]

      # Append Value
      df_field_values = pd.concat([df_field_values, get_field_value_where_filter(df_patient, field)])

    # Append describe
    df_describe.append(df_field_values)

  return df_describe

# Plot Table 1
def plot_table1(df_describes, figsize=10, normalize=True, alpha=0.6):
  """
  Plot Table 1
  """

  for idx, df_describe in enumerate(df_describes):
    # Figure
    fig, axs = plt.subplots(len(df_describe), 1, figsize=(figsize, figsize), sharey=False, tight_layout=False)

    # Loop through fields
    for idy, df_field_values in enumerate(df_describe):
      # Get Label
      if "label" in df_field_values.columns: label=df_field_values["label"].values[0]
      else: label=f"{idx}"

      # Check if field has data
      if df_field_values.empty: continue

      # Contineous Variable
      if df_field_values['data_type'].unique()[0] == 'number':
        # Get Values
        values = df_field_values['value'].to_numpy().flatten()
        # Convert to Number
        values = [float(value) if value is not None else None for value in values]

        axs[idy].hist(values, label=label, density=normalize, alpha = alpha, rwidth=1)
        axs[idy].set_xlabel(f'Tag: {df_field_values["tag"].values[0]}:{df_field_values["field"].values[0]}')
        # Add Text Box
        textstr = f'Missing Data Count: {np.isnan(values).sum()}'
        # these are matplotlib.patch.Patch properties
        props = dict(boxstyle='square', facecolor='white', alpha=0.3)
        axs[idy].text(0.05, 0.95, textstr, transform=axs[idy].transAxes, fontsize=14, verticalalignment='top', bbox=props)
      elif df_field_values['data_type'].unique()[0] == 'categorical' or df_field_values['data_type'].unique()[0] == 'text':
        # Count Frequency
        df_counts = df_field_values['value'].value_counts()
        df_counts = df_counts.sort_values()
        variables = df_counts.index.to_numpy()
        #variables = np.where(variables == None, "", variables) # Remove 'None'
        counts = df_counts.values
        # Normalization
        if normalize: counts = counts/np.sum(counts)
        # Plot
        axs[idy].bar(variables, counts, label=label, alpha = alpha)
        axs[idy].set_xlabel(f'Tag: {df_field_values["tag"].values[0]}:{df_field_values["field"].values[0]}')

  return fig

def link_by_field_value(df: pd.DataFrame, tag_link: dict[str,str], instance: int = 0):
    """Gets tags which have the same field value as the link

    Parameters:
        pt: pd.DataFrame -> dataframe
        tag_link: dict -> Structure of tag_link {'icd10':str, 'tag': str, 'field': str}
        instance: int -> In the event that the tag_link is present multiple times, this specifies which tag to use.
    Return:
        df: pd.DataFrame
    """
    df_linked = pd.DataFrame()
    # Loop through patients
    for patient in df['id'].unique():
        # Get Patient Data
        df_patient = df[df['id'] == patient].copy(deep=True)
        # Get Origin Tags
        df_tags = get_tags_where_filter(df_patient, tag_link)
        # Get Field Value
        df_link = df_tags.loc[(df_tags['field'] == tag_link['field'])]

        if len(df_link) >= 1:
            # Get instance of link
            df_link = df_link.iloc[instance]
            # Get tag_ids where tags tags with field
            tag_ids = df_patient.loc[(df_patient['field'] == df_link['field']) & (df_patient['value'] == df_link['value'])]['tag_id']
            df_patient = df_patient.loc[df_patient['tag_id'].isin(tag_ids)].copy(deep=True)
            # print(df_patient)
            df_linked = pd.concat([df_linked, df_patient])

    return df_linked
