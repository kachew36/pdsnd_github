import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('\nHello! Let\'s explore some US bikeshare data!')
    cities = ['chicago', 'new york city', 'washington']
    while True:
        city = input("\nPlease input the name of a city to analyze (Chicago, New York City, or Washington): ").lower()
        if city in cities:
            print("\nYou have chosen {}. If you did not want to analyze this city, please restart the program.".format(city.title()))
            break
        else:
            print("\nI'm sorry, that is not Chicago, New York City, or Washington. Please try again or restart the program.")

    while True:
        month = input('\nPlease input a month (January, February, ...June) to analyze, or type "all" for all months: ').lower()
        months = ['all','january','february','march','april','may','june']
        if month in months:
            print("\nYou have chosen {}. If you did not want to analyze this month, please restart the program.".format(month.title()))
            break
        else:
            print("\nI'm sorry, that input is not a valid option. Please try again. Ensure your month is within the first 6 months of the year.")
            
    while True:
        day = input('\nPlease input a day of the week to analyze, or type "all" for all days: ').lower()
        days = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        if day in days:
            print("\nYou have chosen {}. If you did not want to analyze this day of the week, please restart the program.".format(day.title()))
            break
        else:
            print("\nI'm sorry, that input is not a valid option. Please try again.")
        
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
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]

    if day != 'all':
        df = df[df['day_of_week'] == day.title()]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    most_common_month = df['month'].mode()[0]
    month_list = ['January', 'February', 'March', 'April', 'May', 'June']
    month_dict = {index + 1: month for index, month in enumerate(month_list)}
    print('\nMost common month: ', month_dict[most_common_month])

    # TO DO: display the most common day of week
    most_common_day = df['day_of_week'].mode()[0]
    print('\nMost common day of the week: ', most_common_day)

    # TO DO: display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    most_common_hour = df['hour'].mode()[0]
    print('\nMost common start hour (in 24 hour format): ', most_common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    popular_start = df['Start Station'].mode()[0]
    print("\nThe most commonly used start station is: ", popular_start)

    # TO DO: display most commonly used end station
    most_common_end_station = df['End Station'].mode()[0]
    print("\nThe most commonly used end station is: ", most_common_end_station)

    # TO DO: display most frequent combination of start station and end station trip
    popular_trip = df.groupby(['Start Station', 'End Station']).size().reset_index(name='counts').nlargest(1, 'counts')
    print("\nThe most frequent combination of start station and end station trip is: \n", popular_trip.iloc[0,0], ' to ', popular_trip.iloc[0,1])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_travel_in_s = df['Trip Duration'].sum()
    print("\nThe total travel time in seconds was: ", total_travel_in_s)
    
    # TO DO: display mean travel time
    mean_travel_time_in_s = df['Trip Duration'].mean()
    print("\nThe average travel time in seconds was: ", mean_travel_time_in_s)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_types = df['User Type'].value_counts()
    print(user_types)
    
    # TO DO: Display counts of gender
    try:
        gender_count = df['Gender'].value_counts()
        print(gender_count)
    except:
        print("\nThere is no gender data for this city!")

    # TO DO: Display earliest, most recent, and most common year of birth

    """Try block created to ensure lack of birth year data does not
    cause an error in the code"""
    try:
        earliest_birth_year = df['Birth Year'].min()
        most_recent_birth_year = df['Birth Year'].max()
        most_common_birth_year = df['Birth Year'].mode()[0]
        print("\nThe earliest year of birth is: ", earliest_birth_year)
        print("\nThe most recent year of birth is: ", most_recent_birth_year)
        print("\nThe most common year of birth is: ", most_common_birth_year)
    except:
        print("\nThere is no data on birth years for this city!")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data(df):
    """Creates a loop to view raw data"""
    raw_data = input('\nWould you like to see 5 rows of raw data? Enter yes or no.\n')
    run_count = 0
    while True:
        if raw_data.lower() != 'no' and run_count*5 < len(df):
            run_count += 1
            print(df.iloc[(run_count - 1) * 5:run_count * 5])
            raw_data = input('\nWould you like to see 5 rows of raw data? Enter yes or no.\n')
        else:
            break
    
    
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)
        
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()