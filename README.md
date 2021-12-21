# AutoKBYT
Tự động khai báo nhiệt độ các ngày trong tuần, chủ nhật tự điền nghỉ ở nhà.

## Installation

Use the command prompt(CMD) to install AutoKBYT. Change directory to maini.exe location, run this command bellow

```bash
main.exe --startup auto install
main.exe start
```
Open services manager to confirm service is running

## Usage
To add new user, open setting.ini file
```python
# Add the 13th user
[USER_13]
id = VNW...
name = Bla..
password = abc...
position_id = 1
position_detail_id = 2
position_areas = 99
```
```python
# Update number of user, very important
# After add the 13th user, now set number_of_user to number_of_user + 1 = 13
[SETTING]
number_of_user = 13
```
Restart AutoKBYT service, it should work
## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
