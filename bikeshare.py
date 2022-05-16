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
     # get user input for city (chicago, new york city, washington)
    while True:
        cities = ['chicago', 'new york city', 'washington']
        city = input("\nChoose from these cities to observe bikeshare data from : Chicago, New York City or Washington \n").lower()
        if city in cities:
            break
        else:
            
            print("\nPlease try again. Choose one of three cities listed above") 

    # get user input for month filter between jan and june or no month filter
    while True:
        months= ['january','february','march','april','may','june','none']
        month = input("\nChoose a month from January to June inclusive, if no month filter is desired type none \n").lower()
        if month in months:
            break
        else:
                
                print("\nPlease try again. Make sure to type out the full spelling of the month")


    # get user input for day of week or no day filter
    while True:
        days= ['monday','tuesday','wednesday','thursday','friday','saturday','sunday','none']
        day = input("\nChoose a day to observe the data from, if no day filter is desired type none \n").lower()         
        if day in days:
            break
        else:
            
            print("\nPlease try again. Make sure to type out the full spelling of the day")    


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
    # load the data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the start time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from start time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name


    # filter by month if applicable
    if month != 'none':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
    
        # filter by month to create the new dataframe
        df = df[df['month'] == month] 

    # filter by day of week if applicable
    if day != 'none':
        # filter by day of week to create the new dataframe
           df = df[df['day_of_week']==day.title()]     
           
    return df


def time_stats(df, month, day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    if month == 'none':
        popular_month = df['month'].mode()[0]
        months = ['January', 'February', 'March', 'April', 'May', 'June']
        popular_month = months[popular_month - 1]

        print("The most popular month was: {}".format(popular_month))

    # display the most common day of week
    if day == 'none':
        popular_day = df['day_of_week'].mode()[0]
        
        print("The most popular day was: {}".format(popular_day))

    # display the most common start hour
    df['Start Hour'] = df['Start Time'].dt.hour
    popular_hour = df['Start Hour'].mode()[0]
    
    print("Most people started at {} o'clock".format(popular_hour))




    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    start_station = df['Start Station'].mode()[0]
    
    print("The most popular station to start as was: {}".format(start_station))

    # display most commonly used end station
    end_station = df['End Station'].mode()[0]
    
    print("The most popular station to end at was: {}".format(end_station))

    # display most frequent combination of start station and end station trip
    df['combo'] = 'started at' + ' ' + df['Start Station']+' '+ 'and ended at' + ' ' + df['End Station']
    popular_combo= df['combo'].mode()[0]
    
    print("The most popular combination of stations {} ".format(popular_combo))
    
    

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_time = df['Trip Duration'].sum()
    m, s = divmod(total_time ,60)
    hr, m = divmod(m, 60)
    
    print("The total time that this service was used: {} hour(s) {} minute(s) {} second(s)".format(hr, m, s))



    # display mean travel time
    avg_time = round(df['Trip Duration'].mean())
    avg_m, avg_s = divmod(avg_time, 60)
    
    if avg_m > 60:
       avg_hr, avg_m = divmod(avg_m, 60)
            
       print("The average trip duration: {} hour(s) {} minute(s) {} second(s)".format(avg_h, avg_m, avg_s))
    else:
            
       print("The average trip duration: {} minute(s) {} second(s)".format(avg_m,avg_s))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()
    
    # display counts of user types
    user_types= df['User Type'].value_counts()
    print("The spread of users are: {}\n".format(user_types))


    # display counts of gender
    if city == 'chicago' or city == 'new york city':
        gender_count= df['Gender'].value_counts()
        print("The spread of gender between the users are: {}".format(gender_count))
    
    # display earliest, most recent, and most common birthdate
        earliest = int(df['Birth Year'].min())
        
        print("The earliest birthdate of a user was {}".format(earliest))
        
        most_recent = int(df['Birth Year'].max())
        
        print("The most recent birthdate of a user was {}".format(most_recent))
        
        common = int(df['Birth Year'].mode()[0])
        
        print("The most common birthdate of the users was {}".format(common))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
def display_data(df):

    # show raw user data on request for the next 5 rows
    while True:
        response = ['yes','no']
        prompt = input("Would you like to view the raw data type yes, if not type no\n").lower()
        if prompt in response:
            if prompt == 'yes':
                # show unaltered data 
                row1 = 0
                row2 = 5
                raw_data = df.iloc[row1:row2,:9]

                print(raw_data)
                break     
        else:

            print("Choose either yes or no please")
        
    if prompt == 'yes':     
            # continue down 5 more rows
            while True:
                prompt_2= input("Would you like to view 5 more rows of raw data type yes, if not type no\n").lower()
                if prompt_2 in response:
                    if prompt_2 == 'yes':
                        row1 += 5
                        row2 += 5
                        raw_data = df.iloc[row1:row2,:9]

                        print(raw_data)
                    else:    
                        break  

    else:
        print("Choose either yes or no please")



def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df, month, day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        display_data(df)
        
        # allow the script to be rerun after using it
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
