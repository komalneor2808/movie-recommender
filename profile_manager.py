# This file manages the user profile dropdown menu
# It handles showing user info, editing profile, changing password, etc.

import streamlit as st
from auth import auth

class ProfileManager:
    def __init__(self):
        # Set up some variables we need to track the profile menu
        if 'show_profile_dropdown' not in st.session_state:
            st.session_state.show_profile_dropdown = False
        if 'profile_tab' not in st.session_state:
            st.session_state.profile_tab = "profile"
    
    def show_profile_button(self):
        # Show the profile icon button in top left corner
        with st.container():
            col1, col2, col3 = st.columns([1, 8, 1])
            with col1:
                if st.button("👤", key="profile_toggle", help="Click to see your profile"):
                    # Toggle the dropdown on/off when clicked
                    st.session_state.show_profile_dropdown = not st.session_state.show_profile_dropdown
                    st.rerun()
    
    def show_profile_menu(self):
        # Only show the dropdown if user clicked the profile button
        if not st.session_state.show_profile_dropdown:
            return
        
        # Create tabs for different profile sections
        with st.container():
            tab1, tab2, tab3 = st.tabs(["My Info", "Change Password", "Settings"])
            
            with tab1:
                self.show_profile_info()
            
            with tab2:
                self.show_password_change()
            
            with tab3:
                self.show_user_settings()
            
            st.markdown("---")
    
    def show_profile_info(self):
        st.subheader("Your Profile")
        
        # Get current user's information from database
        user_info = auth.get_user_info(st.session_state.username)
        if not user_info:
            st.error("Couldn't load your profile info")
            return
        
        # Show current info in two columns
        col1, col2 = st.columns(2)
        
        with col1:
            st.info(f"**Username:** {user_info.get('username', '')}")
            st.info(f"**Email:** {user_info.get('email', '')}")
        
        with col2:
            st.info(f"**Name:** {user_info.get('full_name', 'Not provided')}")
            st.info(f"**Age:** {user_info.get('age', 'Not provided')}")
        
        st.info(f"**Joined:** {user_info.get('created_at', '')}")
        
        # Form to edit profile info
        st.markdown("#### Update Your Info")
        with st.form("edit_profile"):
            new_email = st.text_input("Email", value=user_info.get('email', ''))
            new_name = st.text_input("Full Name", value=user_info.get('full_name', ''))
            new_age = st.number_input("Age", min_value=13, max_value=120, 
                                    value=user_info.get('age') if user_info.get('age') else 25)
            
            if st.form_submit_button("Save Changes", type="primary"):
                success, message = auth.update_user_info(
                    st.session_state.username, new_email, new_name, new_age
                )
                if success:
                    st.success(message)
                    st.rerun()
                else:
                    st.error(message)
        
        # Logout and close buttons
        st.markdown("---")
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("Logout", key="logout_btn"):
                st.session_state.logged_in = False
                st.session_state.username = ""
                st.session_state.show_profile_dropdown = False
                st.success("You've been logged out!")
                st.rerun()
        
        with col2:
            if st.button("Close Menu", key="close_menu"):
                st.session_state.show_profile_dropdown = False
                st.rerun()
    
    def show_password_change(self):
        st.subheader("Change Your Password")
        st.warning("Don't forget your new password!")
        
        # Form for changing password
        with st.form("change_password"):
            current_pwd = st.text_input("Current Password", type="password")
            new_pwd = st.text_input("New Password", type="password")
            confirm_pwd = st.text_input("Confirm New Password", type="password")
            
            if st.form_submit_button("Change Password", type="primary"):
                # Basic validation
                if not current_pwd:
                    st.error("Please enter your current password!")
                elif len(new_pwd) < 6:
                    st.error("New password needs to be at least 6 characters!")
                elif new_pwd != confirm_pwd:
                    st.error("New passwords don't match!")
                else:
                    # Try to change the password
                    success, message = auth.change_password(
                        st.session_state.username, current_pwd, new_pwd
                    )
                    if success:
                        st.success(message)
                        st.balloons()  # Fun celebration!
                    else:
                        st.error(message)
    
    def show_user_settings(self):
        st.subheader("App Settings")
        
        # Get current theme preference
        user_info = auth.get_user_info(st.session_state.username)
        current_theme = user_info.get('theme_preference', 'light') if user_info else 'light'
        
        # Theme selector
        theme_choice = st.selectbox(
            "Pick your theme:",
            options=["light", "dark"],
            index=0 if current_theme == "light" else 1
        )
        
        if st.button("Save Settings", type="primary"):
            if auth.update_theme_preference(st.session_state.username, theme_choice):
                st.session_state.theme = theme_choice
                st.success("Settings saved!")
                st.rerun()
            else:
                st.error("Couldn't save settings, try again")

# Create the profile manager object
profile_manager = ProfileManager()
