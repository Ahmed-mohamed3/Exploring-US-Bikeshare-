import time
import datetime
import calendar
import pandas as pd
import numpy as np
import statistics
from statistics import mode



# Reading the csv files 
chicago = pd.read_csv("chicago.csv")
new_york_city = pd.read_csv("new_york_city.csv")
washington = pd.read_csv("washington.csv")


# dealing with NaN values
# We replace NaN values with the previous value in the column
chicago = chicago.fillna(method = 'ffill', axis = 0)
new_york_city = new_york_city.fillna(method = 'ffill', axis = 0)
washington = washington.fillna(method = 'ffill', axis = 0)


# This function to get the day name of a specific date
def findDay(date):
	day, month, year = (int(i) for i in date.split(' '))
	dayNumber = calendar.weekday(year, month, day)
	days =["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
	return (days[dayNumber])


# This is a function to find the most frequently occurring value using mode.
def most_common(List):
    return(mode(List))


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('               Hello! Let\'s explore some US bikeshare data!               ')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        try:
            print ( "\nPlease choose which city you want to search in its data: " )
            print ("1- Chicago \n2- New York. \n3- Washington. ")
            city = int(input("Please put the city number: "))
        except ValueError:
            print("\nSorry, you must only choose 1, 2, or 3.")
            continue
    
        if (city < 1 or city >3 ):
            print("\nSorry, your response must be 1, 2, or 3.")
            continue
        else:
            break
    print('-'*40, "\n")
    # get user input for month (all, january, february, ... , june)
    while True:
        try:
            print ( "\nPlease choose which month would you like to filter its data: " )
            print ( "1- January. \n2- February. \n3- March. \n4- April. \n5- May. \n6- June. \n7- all. ( if you donot want to choose a spacific month )")
            month = int (input("Please put the month number: "))
        except ValueError:
            print("\nSorry, you must only choose the number from 1 to 7.")
            continue
    
        if (month < 1 or month >7):
            print("\nSorry, your response must be in range from 1 to 7.")
            continue
        else:
            break
    print('-'*40, "\n")
    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        try:
            print ( "Please choose which day would you like to filter its data: " )
            print ("1- Moday. \n2- Tuesday. \n3- Wednesday. \n4- Thursday. \n5- Friday. \n6- saturday. \n7- sunday. \n8- all. ( if you donot want to choose a spacific month )")
            day = int (input("\nPlease put the day number: "))
        except ValueError:
            print("\nSorry, you must only choose numbers from 1 to 8.")
            continue
    
        if (day < 1 or day> 8):
            print("\nSorry, your response must be in range from 1 to 8.")
            continue
        else:
            break
    print('-'*40, "\n")
    
    if (city == 1): city ="chicago"
    elif (city == 2): city ="new york city"
    elif (city == 3): city ="washington"
        
    if (month == 1): month = "january"
    elif (month == 2): month ="february" 
    elif (month == 3): month = "march"
    elif (month == 4): month = "april"
    elif (month == 5): month = "may"
    elif (month == 6): month = "june"
    elif (month == 7): month = "all"
    
    if (day == 1): day = "monday"
    elif (day == 2): day = "tuesday"
    elif (day == 3): day = "wednesday"
    elif (day == 4): day = "thursday"
    elif (day == 5): day = "friday"
    elif (day == 6): day = "saturday"
    elif (day == 7): day = "sunday"
    elif (day == 8): day = "all"
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
    if (city == "chicago"):
        data = chicago
    elif (city == "new york city"):
        data = new_york_city
    elif (city == "washington"):
        data = washington
    
    if (day == 'all'and month=='all'):
        return data
    
    data['day'] = pd.DatetimeIndex(data['Start Time']).day
    data['month'] = pd.DatetimeIndex(data['Start Time']).month
    data['year'] = pd.DatetimeIndex(data['Start Time']).year
    data["final"]= data["day"].astype(str) +' '+ data["month"].astype(str) +' '+ data["year"].astype(str)
        
    term = []
    for date in data['final']:
        x = findDay(date)
        term.append(x)
            
    df = pd.DataFrame (term, columns = ['days'])
    result = pd.concat([data, df], axis=1)
    result.set_index('days', inplace=True)
    
    #check if the day = all
    if day != 'all':    
        result = result.loc[[day]]
    
    #check if the month = all        
    if month != 'all':
        result["months"]= result["month"].astype(str)
        result.set_index('months', inplace=True)
    
        if (month == "january"): month = 1  
        elif (month == "february" ): month = 2
        elif (month == "march"): month = 3
        elif (month == "april"): month = 4
        elif (month == "may"): month = 5
        elif (month == "june"): month = 6
        elif (month == "all"): month = 7
        result = result.loc[[str(month)]]
    result = result.drop(['month'], axis = 1)
    result = result.drop(['day', 'final', 'year'], axis = 1)
    
    return result


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    
    
    # display the most common month
    df['month'] = pd.DatetimeIndex(df['Start Time']).month
    col_one_list = df['month'].tolist()
    print ("the most common month is: ",datetime.date(1900, most_common(col_one_list), 1).strftime('%B') )
    
    
    # display the most common day of week
    df['day'] = pd.DatetimeIndex(df['Start Time']).day
    df['year'] = pd.DatetimeIndex(df['Start Time']).year
    df["final"]= df["day"].astype(str) +' '+ df["month"].astype(str) +' '+ df["year"].astype(str)
    
    term = []
    for date in df['final']:
        x = findDay(date)
        term.append(x)
    
    print ("the most common day is: ",most_common(term) )
    

    # display the most common start hour
    df['hour'] = pd.DatetimeIndex(df['Start Time']).hour
    col_one_list = df['hour'].tolist()
    print ("the most common hour is: ",most_common(col_one_list) )
      
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40,"\n")


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    col_one_list = df['Start Station'].tolist()
    print ("the most common start station is: ",most_common(col_one_list) )

    # display most commonly used end station
    col_one_list = df['End Station'].tolist()
    print ("the most common end station is: ",most_common(col_one_list) )


    # display most frequent combination of start station and end station trip
    df["compination"] = df["Start Station"] + " "+ df["End Station"]
    col_one_list = df['compination'].tolist()
    print ("the most frequent combination of start station and end station trip is: ",most_common(col_one_list) )
    

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total = df['Trip Duration'].sum()
    print("Total travel time :", total)

    # display mean travel time
    mean = df['Trip Duration'].mean()
    print("Mean travel time: ", mean)
    

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    count_user_type = df['User Type'].value_counts(ascending=True)
    print("Counts of each User Type:\n",count_user_type)
    
    print('*'*20,"\n")

    # Display counts of gender
    if 'Gender' in df.columns:
        count_Gender = df['Gender'].value_counts(ascending=True)
        print("Counts of each Gender:\n", count_Gender)

    print('*'*20,"\n")
    
    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        birth_year_column = df["Birth Year"]
        most_recent = birth_year_column.max()
        print("The most recent birth year is: ", most_recent)
        
        
        most_earliest = birth_year_column.min()
        print("The most earliest birth year is: ", most_earliest)     
    
        col_one_list = birth_year_column.tolist()
        print ("The most common year is: ", most_common(col_one_list))
    

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40,"\n")
    
    
    
def display_data(df):
    """Displays raw bikeshare data."""
    
    row_length = df.shape[0]

    for i in range(0, row_length, 5):
        
        yes = input('\nWould you like to display particular user trip data? ( yes or no )\n')
        if yes.lower() != 'yes':
            break
        
        row_data = df.iloc[i: i + 5]
        
        print (row_data.head(5))

def main():
    while True:
        
         
        city, month, day = get_filters()
        if (city == "chicago"):
            df = chicago
        elif (city == "new york city"):
            df = new_york_city    
        elif (city == "washington"):
            df = washington
        answer = input("Do you want to see the data after filtering it? (yes or no)\n")
        if answer.lower() == 'yes':    
            df = load_data(city, month, day)
            print(df)
        
        answer = input("\nDo you want to displays statistics on the most frequent times of travel? (yes or no)\n")
        if answer.lower() == 'yes':    
            time_stats(df)
        
        answer = input("\nDo you want to displays statistics on the most Popular Stations and Trip? (yes or no)\n")
        if answer.lower() == 'yes':
            station_stats(df)
        
        answer = input("\nDo you want to displays statistics on the total and average trip duration? (yes or no)\n")
        if answer.lower() == 'yes':
            trip_duration_stats(df)
        
        answer = input("\nDo you want to displays statistics on bikeshare users? (yes or no)\n")
        if answer.lower() == 'yes':
            user_stats(df)

        display_data(df)
        
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break
        


if __name__ == "__main__":
 	main()
