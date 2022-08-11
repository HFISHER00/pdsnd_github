import time
import pandas as pd
import numpy as np


CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
            
CITIES = ['chicago', 'new york city', 'washington']

MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'all']

DAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday', 'all']


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    valid_city = 0
    city = input("Enter a city (Chicago, New York City, Washington): ").lower()
    while valid_city == 0:
        if city in CITIES:
            valid_city += 1
        else:
            city = input("Not a valid city. Please enter one of Chicago, New York City or Washington: ").lower()
        

    # get user input for month (all, january, february, ... , june)
    valid_month = 0
    
    # turn MONTHS list to lowercase
    month_list = MONTHS.copy()
    lc_months = turn_list_lowercase(month_list)
    
    month = input("Enter a month (all or specific month): ").lower()
    while valid_month == 0:
        if month in lc_months:
            valid_month += 1
        else: 
            month = input("Not a valid month, please try again. Enter all or specific month: ").lower()
    
    # get user input for day of week (all, monday, tuesday, ... sunday)
    valid_day = 0

    # turn DAYS list to lowercase
    day_list = DAYS.copy()
    lc_days = turn_list_lowercase(day_list)

    day = input("Enter a day of the week (all or specific day): ").lower()
    while valid_day == 0:
        if day in lc_days:
            valid_day += 1
        else:
            day = input("Not a valid day, please try again. Enter all or specific day: ").lower()

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    if city == 'chicago':
        df = pd.read_csv(r'./chicago.csv')
    elif city == 'new york city':
        df = pd.read_csv(r'./new_york_city.csv')
    elif city == 'washington':
        df = pd.read_csv(r'./washington.csv')

    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # create month column
    df['mm'] = df['Start Time'].dt.month
    
    # create a day of week column - monday = 0
    df['dd'] = df['Start Time'].dt.dayofweek

    # create an hour of day column (for start time)
    df['hr'] = df['Start Time'].dt.hour

    # specify which month/s
    if month == 'january':
        df = df[df['mm'] == 1]
    elif month == 'february':
        df = df[df['mm'] == 2]
    elif month == 'march':
        df = df[df['mm'] == 3]
    elif month == 'april':
        df = df[df['mm'] == 4]
    elif month == 'may':
        df = df[df['mm'] == 5]
    elif month == 'june':
        df = df[df['mm'] == 6]
    
    # specify which day/s
    if day == 'monday':
        df = df[df['dd'] == 0]
    elif day == 'tuesday':
        df = df[df['dd'] == 1]
    elif day == 'wednesday':
        df = df[df['dd'] == 2]
    elif day == 'thursday':
        df = df[df['dd'] == 3]
    elif day == 'friday':
        df = df[df['dd'] == 4]
    elif day == 'saturday':
        df = df[df['dd'] == 5]
    elif day == 'sunday':
        df = df[df['dd'] == 6]
        
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    common_month = df['mm'].value_counts().idxmax()
    month_name = num_to_month_convert(common_month)
    print("The most common month: " + month_name)

    # display the most common day of week
    common_day = df['dd'].value_counts().idxmax()
    day_name = num_to_day_convert(common_day)
    print("The most common day: " + day_name)

    # display the most common start hour
    common_hour = df['hr'].value_counts().idxmax()
    print("The most common start hour: " + str(common_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start_station = df['Start Station'].value_counts().idxmax()
    print("The most common start station: " + common_start_station)

    # display most commonly used end station
    common_end_station = df['End Station'].value_counts().idxmax()
    print("The most common end station: " + common_end_station)

    # display most frequent combination of start station and end station trip
    common_combo = df[['Start Station', 'End Station']].mode().loc[0]
    print("Most common combination of stations: {} to {}".format(common_combo[0], common_combo[1]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_time = df['Trip Duration'].sum()
    print("The total travel time: " + str(total_time))

    # display mean travel time
    amount_of_trips = len(df.index)
    average_trip = total_time / amount_of_trips
    print("The mean travel time: " + str(average_trip))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print("User Type Counts:")
    user_counts = df['User Type'].value_counts()
    new_data = df['User Type'].value_counts().index.tolist()
    i = 0
    while i < len(user_counts):
        print(new_data[i] + ': ' + str(user_counts[i]))
        i += 1
    print('\n')

    # Display counts of gender and birth year - note Washington didn't record these
    if city == 'washington':
        print("Sorry, gender and birth year was not recorded.")
    else:
        # Display gender data
        print("Gender Counts: ")
        gender_counts = df['Gender'].value_counts()
        gender_types = df['Gender'].value_counts().index.tolist()
        j = 0
        while j < len(gender_counts):
            print(gender_types[j] + ': ' + str(gender_counts[j]))
            j += 1
        print('\n')

        # Number of people putting NaN for gender
        num_na_gender =  df['Gender'].isnull().sum().sum()
        print("The number of NaN for Gender: " + str(num_na_gender))

        # Display earliest, most recent, and most common year of birth
        # incase NaN is a result
        birth_years = df['Birth Year'].dropna()
        
        # Year of birth for oldest person
        earliest_year = birth_years.min()
        print("\nThe earliest birth year: " + str(earliest_year))
        
        # Year of birth for youngest person
        latest_year = birth_years.max()
        print("The most recent birth year: " + str(latest_year))
        
        # Most common birth year
        common_year = birth_years.value_counts().idxmax()
        print("The most common birth year: " + str(common_year))

        # Number of people putting NaN for birth year
        num_na_year =  df['Birth Year'].isnull().sum().sum()
        print("The number of NaN for Birth Year: " + str(num_na_year))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def num_to_month_convert(number):
    """Converts number to corresponding month name"""

    month = MONTHS[number - 1]

    return month


def num_to_day_convert(number):
    """Converts number to corresponding day of the week"""

    day = DAYS[number]
    
    return day


def turn_list_lowercase(listx):
    """Converts all string in list to lowercase"""

    for i in range(len(listx)):
        listx[i] = listx[i].lower()

    return listx


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        
        rows_shown = 5
        see_data = input('\nWould you like to see raw data? Enter yes or no.\n').lower()
        while see_data == 'yes':
            print(df.head(rows_shown))
            see_data = input('\nWould you like to see more data? Enter yes or no.\n').lower()
            rows_shown += 5
            if rows_shown > len(df):
                print("Sorry, there is no more raw data.")
                see_data = 'no'
            
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
