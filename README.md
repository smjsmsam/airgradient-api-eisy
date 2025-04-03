
# AirGradient Node Server

A simple node server for connection to the AirGradient air quality sensor using AirGradientAPI.

## Installation
See instructions for loading a node below

### Node Settings
The settings for this node are:

#### Short Poll
   * How often to increment the API request
#### Token
   * Client token, which can be found on the AirGradient dashboard.

#### Index
   * Based on the order of AirGradient devices on client account, 0-indexed.


## Requirements

1. Polyglot V3.
2. ISY firmware 5.3.x or later

# Instructions for Loading a Node 

The steps written above pretty much follow the same documentation from UD on https://developer.isy.io/ 
1. Email sales@universal-devices.com to sign up the isy portal account as a developer using the format listed in this website: https://developer.isy.io/docs/getstarted/signup
2. Connect the eisy to wifi using the UD Mobile app.
3. Connect the eisy to a monitor and keyboard.
4. Log in using the default login admin - admin.
5. Input start.win to the terminal 
6. Open the file system and create the node server folder in home/admin/workspace/plugin-dev , it is recommended to clone a sample (we used https://github.com/UniversalDevicesInc/udi-example2-poly ) and edit the code from there.
7. On a separate device (mac/pc) download and run iox finder. Make sure the device is on the same wifi.
8. The eisy should show up automatically on the iox finder. Click on it to access polyglot v3.
9. PG3 should open a new tab on your browser. If it shows a warning, proceed anyway.
10. Log in, if for the first time the user is admin and the password is admin. It can be edited and the credentials also apply for the admin console login. (ours is markwalter - uciocc23)
11. Assuming the account is a developer account already (my email is added to our account as the developer) click on "add new plugin" from the development tab.
12. Fill in the relevant information and submit for development/production.
13. Go to the production store and install the node server onto the dashboard.
14. Fill in the relevant parameters for the node server in the configuration tab.
15. Now the node server is made and available to debug/test/run.



# Release Notes

- 1.0.1 03/16/2024
   - Fixed errors for invalid parameters
   - Added documention
- 1.0.0 03/12/2024
   - Initial version published to github
