from lib import driver_connection
from lib import driver_read
# test driver_connection and driver_read
driver = driver_connection.driver_connection()
read = driver_read.driver_read(driver)
print(read._get_speed())
print(read._get_current())
print(read._get_DI_status())
print(read._get_DO_status())
print(read._get_ERROR())
#test successful, 0213 19:40
#%%
from lib import driver_setting
setting = driver_setting.driver_setting(driver)
setting._driver_address()
setting._driver_restore()
