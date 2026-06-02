import time
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}


def get_valid_input(valid_input):
    """
    Helper function to identify valid user input based on given list of values.

    Args:
        (list[str]) valid_input: A list of strings of valid user input
    Returns:
        (str) choice - valid user input
    """
    # get user input
    choice = input("Your choice: ").lower()

    # validate user input
    if choice in valid_input:
        return choice
    else:
        # user input is not valid - request valid input recursive
        print("Sorry this is not a valid input. It must be one of the following "
              "values:")
        print(valid_input)
        choice = get_valid_input(valid_input)
    return choice


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no
                    month filter
        (str) day - name of the day of week to filter by, or "all" to apply
                    no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    # get user input for city (chicago, new york city, washington).
    print("Which city to you want to analyze? "
          "Choose 'c' for Chicago, 'nyc' for New York City or 'w' for "
          "Washington: ")
    user_input = get_valid_input(["c", "nyc", "w"])

    match user_input:
        case "c":
            city = "chicago"
        case "nyc":
            city = "new york city"
        case "w":
            city = "washington"

    # get user input for month (all, january, february, ... , june)
    print("Which month to you want to analyze? Choose a month between "
          "'january' and 'june' or 'all' if you want to include all months: ")
    month = get_valid_input(["january", "february", "march", "april",
                             "may", "june", "all"])

    # get user input for day of week (all, monday, tuesday, ... sunday)
    print("Which day to you want to analyze? Choose a day between 'monday' "
          "and 'sunday' or 'all' if you want to include all days: ")
    day = get_valid_input(["monday", "tuesday", "wednesday", "thursday",
                           "friday", "saturday", "sunday", "all"])

    print('-'*30)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if
    applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply
                    no month filter
        (str) day - name of the day of week to filter by, or "all" to
                    apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    # load data file into a dataframe
    df = pd.read_csv(city.replace(" ", "_") + '.csv')

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.dayofweek

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month)+1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday',
                'saturday', 'sunday']
        day = days.index(day)
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    print('Most common month of travel: '
          + pd.to_datetime(df['Start Time']).dt.month_name().mode()[0])

    # display the most common day of week
    print('Most common day of week of travel: '
          + pd.to_datetime(df['Start Time']).dt.day_name().mode()[0])

    # display the most common start hour
    print('Most common start hour of travel: '
          + str(pd.to_datetime(df['Start Time']).dt.hour.mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*30)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Display most commonly used start station
    print('Most commonly used start station: '
          + str(df['Start Station'].mode()[0]))

    # Display most commonly used end station
    print('Most commonly used end station: '
          + str(df['End Station'].mode()[0]))

    most_common_pair = df.value_counts(['Start Station',
                                        'End Station']).nlargest(1)
    print("Most frequent trip: " + str(most_common_pair.index[0][0])
          + " -> " + str(most_common_pair.index[0][1]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*30)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Display total travel time
    print("Total travel time (minutes): "
          + str(int(df['Trip Duration'].sum())))

    # Display mean travel time
    print("Mean trip duration (minutes): "
          + str(int(df['Trip Duration'].mean())))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*30)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types

    ut_count = df[df['User Type'] != 'Dependent']['User Type'].value_counts()
    ut_count.index.name = None
    ut_count.name = None
    print("User type counts:\n" + ut_count.to_string())
    print('-'*10)

    # Display counts of gender if available
    if 'Gender' in df.columns:
        gender_count = df[df['Gender'] != 'Dependent']['Gender'].value_counts()
        gender_count.index.name = None
        gender_count.name = None
        print("Gender counts:\n" + gender_count.to_string())
    else:
        print("No gender data available in this dataset.")

    print('-'*10)

    # Display earliest, most recent, and most common year of birth if available
    if 'Gender' in df.columns:
        print("Earliest year of birth: "
              + str(int(df['Birth Year'].min())))
        print("Most recent year of birth: "
              + str(int(df['Birth Year'].max())))
        print("Most common year of birth: "
              + str(int(df['Birth Year'].mode()[0])))
    else:
        print("No birth year data available in this dataset.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*30)


def raw_data(df):
    """Displays raw data in user defined slices with possibility to skip."""

    # is there data to be displayed
    total = len(df)
    start_index = 0  # start index

    if total == 0:
        print("There are no rows to display.")
        return

    # Ask user if raw data shall be displayed
    print("Do you want to see raw data? "
          "Choose 'yes' or 'no': ")
    user_input = get_valid_input(["yes", "no"])

    if user_input == "yes":
        # if yes, ask user how many rows at a time (valid input 1-100)
        print("How many rows do you want to be displayed? "
              "Choose '1', '5' or '10': ")
        slice_size = int(get_valid_input(["1", "5", "10"]))

        print('\nStart displaying raw data in slices of '
              + str(slice_size) + ' rows ...\n')

        # while loop with chunks
        while start_index < total:
            end_index = min(start_index + slice_size, total)
            print(f"\nShowing rows {start_index} to {end_index - 1} of"
                  f"{total - 1} (slice size={slice_size})")
            # display raw data in chunks
            print(df.iloc[start_index:end_index])

            #  continue with next slice or break?
            print(f"\nDo you want to see the next {slice_size} rows of data?"
                  " Enter 'yes' or 'no'.")
            user_input = get_valid_input(["yes", "no"])

            if user_input != 'yes':
                print(f"Stopped at index {start_index}.")
                break

            # calculate new start index for the next loop
            start_index = end_index

            if start_index >= total:
                print("\nEnd of data.")

    print('-'*30)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)

        print("\nWould you like to restart? Enter 'yes' or 'no'.\n")
        restart = get_valid_input(["yes", "no"])
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
