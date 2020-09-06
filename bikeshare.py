

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
    print('Hello! Let\'s explore some US bikeshare data!')
    print('please make input match a choice in the lists provided.  ')
    print()
    print('Please input the city name for the data to be explored: ')  
    city=input('Type a name from this list: chicago, washington or new york city:  ').lower()
    print()
    print('Please input the month name for the data to be explored: ') 
    month=input('Type a month from this list: :(all, january, february,march april, may, june:  ').lower()
    day=input('Enter the Day of week to investigate (all, monday, tuesday, wednsday,thursday, friday, saturday, sunday:  ').lower()
    """
    Verify user inputs match expected values from lists.
    Ask user to correct inputs that are not valid
    Set a counter -count_bad_inputs that counts the number of user input errors.
    Counter to be used to break out of re-input loop upon more that 3 bad input iterations.
    
    """
    count_bad_inputs = int(0)
    months_inp_valid = ['january', 'february', 'march', 'april', 'may', 'june','all']
    cities_inp_valid = ['chicago', 'washington','new york city']
    days_inp_valid = ['sunday','monday', 'tuesday', 'wednsday', 'thursday','friday','saturday','all']
    
    while (city not in cities_inp_valid or month not in months_inp_valid or day not in days_inp_valid) and count_bad_inputs < 3:
        count_bad_inputs+=1
        if city not in cities_inp_valid:
            print()
            print('please input a valid city name')   
            city=input('Enter the City for the data you want to explore chicago, washington or new york city:  ').lower()
    
        if month not in months_inp_valid:
            print()
            print('please input a valid month')   
            month=input('Enter the month to investigate:(all, january, february,march april, may, june:  ').lower()
        
        if day not in days_inp_valid:
            print()
            print('please input a valid weekday')
            day=input('Enter the Day of week to investigate (all, monday, tuesday, wednsday,thursday, friday, saturday, sunday:  ').lower() 
       
        if count_bad_inputs >2:
             print('strike three: you have entered more than three improper inputs for city, month, or day')
             break
             
    
    print('-'*40)
    return city, month, day, count_bad_inputs


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
    #load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city]) 

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday
    df['hour_of_day'] = df['Start Time'].dt.hour   
    df['trip']=df['Start Station']+' - to - '+df['End Station']
        
    
    # filter by month if applicable
    # use the index of the months list to get the corresponding int
    
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    if month !='all':
        month = months.index(month)+1
        # filter by month and create the new dataframe
        df = df.loc[df['month']==month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week and create the new dataframe
        days = ['sunday','monday', 'tuesday', 'wednsday', 'thursday','friday','saturday']
        day = days.index(day)
        df = df.loc[df['day_of_week']==day]   
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    
    #use these reference lists in order to display month and day names from index numbers 
    days1 = ['sunday','monday', 'tuesday', 'wednsday', 'thursday','friday','saturday']
    months1 =['january', 'february', 'march', 'april', 'may', 'june']
    
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # calculate the most common month
    popular_month = df['month'].mode().get(0)
   
    # calculate the most common day of week
    popular_weekday = df['day_of_week'].mode().get(0)

    # calculate the most common start hour from 0 to 23
    popular_hour = df['hour_of_day'].mode().get(0)
    
    #print out the popular time calculations
    print('The most popular hour of day is: {}'.format(popular_hour))
    print('The most popular day of week is: ', (popular_weekday+1),' = ', days1[popular_weekday])
    print('The most popular month is: ', (popular_month),'  = ',months1[popular_month-1])
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)



def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    # display most commonly used start station
    print('The most popular starting station for trips is:'  )
    start_sta =(df['Start Station'].value_counts())
    start_sta_max = start_sta.nlargest(1)
    print(start_sta_max.index.values)
    print()
    
    # display most commonly used end station
    print('The most popular ending station for trips is:'  )
    end_sta =(df['End Station'].value_counts())
    end_sta_max = end_sta.nlargest(1)
    print(end_sta_max.index.values)
    print()
    
    # display most frequent combination of start station and end station trip
    trip_ends =(df['trip'].value_counts())
    print('The most popular trip is:'  )
    trip_ends_max = trip_ends.nlargest(1)
    print(trip_ends_max.index.values)
    
    
        
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
    
def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time in minutes
    print('The total sum of trip durations for the selected City / Time Interval is: {} minutes'.format(df['Trip Duration'].sum()))
    print()
    # display mean travel time in minutes
    print('The average trip duration for the selected City / Time Interval is: {} minutes'.format(round(df['Trip Duration'].mean(),3)))
    

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df,city):
    """Displays statistics on bikeshare users."""
    print('\nCalculating User Stats...\n')
    start_time = time.time()
    # Display counts of user types
    user_tipes =(df['User Type'].value_counts())
    print('Counts of User Categories')
    print(user_tipes)
    print()
    #washington has no columns for Gender nor Birth Year in DFrame
    if city != 'washington':
        # Display counts of gender
        print('Counts of User Genders')
        user_gend =(df['Gender'].value_counts())
        print(user_gend)
        # Display earliest, most recent, and most common year of birth
        print('\nThe youngest passenger was born in: {}'.format(int(df['Birth Year'].max())))
        print('The oldest passenger was born in: {}'.format(int(df['Birth Year'].min())))
        print('The average-aged passenger was born in: {}'.format(int(df['Birth Year'].mean())))
        print('The most common birth year for passengers is: {}'.format(int(df['Birth Year'].mode())))
                
    else:
        print('Note that washinton does not have data for Gender and Birthdate')
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
   
def see_raw_data(df):
    """Displays 5 rows of raw data upon user request."""
    print('see raw data')
    see_rawd=input('Do you wish to see 5 lines of the original data?: enter yes or no?:  ')
    if see_rawd =='yes':
        print(df.head())
    else:
        print('ok- no raw data will be displayed')
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    #call all functions; break if #bad user inputs > 3
    #break if no data to analyze
    while True:
        city, month, day, count_bad_inputs = get_filters()
        if count_bad_inputs >2:
            break
        df = load_data(city, month, day)
        if df.empty == True:
            print('No trip data for City and Dates Selected')
            break
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)
        see_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
