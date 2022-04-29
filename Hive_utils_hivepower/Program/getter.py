import updater_mod
import multiprocessing
import time
import schedule
import smtplib, ssl

#100%_hivepower_0%


# object armoredbanana
def user_1():
    user1 = updater_mod.Hive_power_tracker(username = "armoredbanana", email_address = "thomas.kidd@okstate.edu", treshold = 0, resend_time = 60) # treshold when hive power is 100%, resends email when full after 6 hours

# object trostparadox
def user_2():
    user2 = updater_mod.Hive_power_tracker(username = "trostparadox", email_address = "trostparadox@gmail.com", treshold = 216, resend_time = 120) # treshold when hive power is 97%, resends email when full after 2 hours

# object bhanutejap
def user_3():
    user3 = updater_mod.Hive_power_tracker(username = "bhanutejap", email_address = "bhanutejap20@gmail.com", treshold = 0, resend_time = 1440) # treshold when hive power is 100%, resends email when full after 24 hours


process_1 = multiprocessing.Process(target=user_1)
process_2 = multiprocessing.Process(target=user_2)
process_3 = multiprocessing.Process(target=user_3)

process_1.start()
process_2.start()
process_3.start()




