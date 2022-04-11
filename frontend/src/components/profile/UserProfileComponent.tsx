import React, { PureComponent } from 'react';
import withRouter from '../../helper/RouterHelper';
import HeaderComponent from '../HeaderComponent';
import FooterComponent from '../FooterComponent';
import withAppState, { ReduxState } from '../../helper/ReduxHelper';
import { AppState } from '../../redux/Store';

import './UserProfileComponent.scss';

class UserProfileComponent
  extends PureComponent <ReduxState> {
  render() {
    return (
      <div className="user-profile">
        <HeaderComponent pageTitle="My Profile" />
        <div className="main">
          User
        </div>
        <FooterComponent />
      </div>
    );
  }
}

export default withRouter(withAppState(UserProfileComponent, (state: AppState) => state));
