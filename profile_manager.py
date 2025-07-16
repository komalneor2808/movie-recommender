import streamlit as st
from auth import auth

class ProfileManager:
    def __init__(self):
        if 'show_profile_dropdown' not in st.session_state:
            st.session_state.show_profile_dropdown = False
        if 'profile_tab' not in st.session_state:
            st.session_state.profile_tab = "profile"
    
    def render_profile_icon(self):
        with st.container():
            col1, col2, col3 = st.columns([1, 8, 1])
            with col1:
                if st.button("👤", key="profile_toggle", help="Click to open profile menu"):
                    st.session_state.show_profile_dropdown = not st.session_state.show_profile_dropdown
                    st.rerun()
    
    def render_profile_dropdown(self):
        if not st.session_state.show_profile_dropdown:
            return
        
        with st.container():
            tab1, tab2, tab3 = st.tabs(["Profile", "Password", "Preferences"])
            
            with tab1:
                self.render_profile_tab()
            
            with tab2:
                self.render_password_tab()
            
            with tab3:
                self.render_preferences_tab()
            
            st.markdown("---")
    
    def render_profile_tab(self):
        st.subheader("Profile Information")
        
        user_info = auth.get_user_info(st.session_state.username)
        if not user_info:
            st.error("Could not load user information")
            return
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.info(f"**Username:** {user_info.get('username', '')}")
            st.info(f"**Email:** {user_info.get('email', '')}")
        
        with col2:
            st.info(f"**Full Name:** {user_info.get('full_name', 'Not set')}")
            st.info(f"**Age:** {user_info.get('age', 'Not set')}")
        
        st.info(f"**Member since:** {user_info.get('created_at', '')}")
        
        st.markdown("#### Edit Profile")
        with st.form("profile_edit_form"):
            new_email = st.text_input("Email", value=user_info.get('email', ''))
            new_full_name = st.text_input("Full Name", value=user_info.get('full_name', ''))
            new_age = st.number_input("Age", min_value=13, max_value=120, 
                                    value=user_info.get('age') if user_info.get('age') else 25)
            
            if st.form_submit_button("Update Profile", type="primary"):
                success, message = auth.update_user_info(
                    st.session_state.username, new_email, new_full_name, new_age
                )
                if success:
                    st.success(message)
                    st.rerun()
                else:
                    st.error(message)
        
        st.markdown("---")
        st.markdown("#### Actions")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("Logout", key="profile_logout", help="Logout from your account"):
                st.session_state.logged_in = False
                st.session_state.username = ""
                st.session_state.show_profile_dropdown = False
                st.success("Logged out successfully!")
                st.rerun()
        
        with col2:
            if st.button("Close", key="profile_close", help="Close profile menu"):
                st.session_state.show_profile_dropdown = False
                st.rerun()
    
    def render_password_tab(self):
        st.subheader("Change Password")
        st.warning("Make sure to remember your new password!")
        
        with st.form("password_change_form"):
            old_password = st.text_input("Current Password", type="password", 
                                       help="Enter your current password to verify your identity")
            new_password = st.text_input("New Password", type="password",
                                       help="Password must be at least 6 characters long")
            confirm_new_password = st.text_input("Confirm New Password", type="password")
            
            if st.form_submit_button("Change Password", type="primary"):
                if not old_password:
                    st.error("Please enter your current password!")
                elif len(new_password) < 6:
                    st.error("New password must be at least 6 characters long!")
                elif new_password != confirm_new_password:
                    st.error("New passwords don't match!")
                else:
                    success, message = auth.change_password(
                        st.session_state.username, old_password, new_password
                    )
                    if success:
                        st.success(message)
                        st.balloons()
                    else:
                        st.error(message)
    
    def render_preferences_tab(self):
        st.subheader("Preferences")
        
        user_info = auth.get_user_info(st.session_state.username)
        current_theme = user_info.get('theme_preference', 'light') if user_info else 'light'
        
        theme_option = st.selectbox(
            "Choose your preferred theme:",
            options=["light", "dark"],
            index=0 if current_theme == "light" else 1,
            help="Select between light and dark theme for the application"
        )
        
        if st.button("Save Preferences", type="primary"):
            if auth.update_theme_preference(st.session_state.username, theme_option):
                st.session_state.theme = theme_option
                st.success("Preferences saved successfully!")
                st.rerun()
            else:
                st.error("Failed to save preferences. Please try again.")

profile_manager = ProfileManager()
