""" User Management Module

This module reads the 'oh3c' file and manage all users's login info.

"""
import ConfigParser
__all__ = ["usermgr"]


class UserMgr:
    def __init__(self):
        self.users_info_file_path = '/etc/config/oh3c'
        self.cf = ConfigParser.ConfigParser()
        self.cf.read(self.users_info_file_path)
       
    def get_user_number(self):
        """ Get the number of users in user info file
        """
        return len(self.cf.sections())

    def get_users_info(self):
        """ Get an outline of all users info,
        including account, device and binging MAC-address
        """
        users_info = []
        for account in self.cf.sections():
            device = self.cf.get(account, 'device')
            mac_address = self.cf.get(account, 'mac_address')
            method = self.cf.get(account, 'method')
            users_info.append((account, device, mac_address, method))

        return users_info
    
    def delete_user(self, user_name):
        self.cf.remove_section(user_name)
        self.save_config()
    
    def create_user(self, user_info):
        self.cf.add_section(user_info[0])
        self.update_user_info(user_info)

    def update_user_info(self, user_info):
        self.cf.set(user_info[0], 'password', user_info[1])
        self.cf.set(user_info[0], 'device', user_info[2])
        self.cf.set(user_info[0], 'mac_address', user_info[3])
        self.cf.set(user_info[0], 'method', user_info[4])
        self.save_config()
        
    def save_config(self):
        users_config = open(self.users_info_file_path, 'w')
        self.cf.write(users_config)
        users_config.close()

    # user_info_index = ['account', 'password', 'device','mac_address']
    def get_user_info(self, index):
        account = self.cf.sections()[index]
        password = self.cf.get(account, 'password')
        device = self.cf.get(account, 'device')
        mac_address = self.cf.get(account, 'mac_address')
        method = self.cf.get(account, 'method')
        return account, password, device, mac_address, method


