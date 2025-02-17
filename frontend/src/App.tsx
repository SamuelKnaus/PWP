import React from 'react';
import './App.scss';
import {
  unstable_HistoryRouter as HistoryRouter, Routes, Route, Navigate,
} from 'react-router-dom';
import { Spinner } from 'react-bootstrap';
import MovieListComponent from './components/movies/MovieListComponent';
import Fetch from './helper/Fetch';
import MovieDetailComponent from './components/movies/MovieDetailComponent';
import { MasonDoc } from './models/MasonDoc';
import withAppState, { ReduxState } from './helper/ReduxHelper';
import {
  SET_ADD_CATEGORY_URL, SET_ADD_MOVIE_URL, SET_ADD_USER_URL,
  SET_ALL_CATEGORIES_URL, SET_ALL_MOVIES_URL, SET_ALL_USERS_URL,
  SET_CURRENT_USER_URL, SET_LOGIN_URL,
} from './redux/Reducer';
import LoginComponent from './components/authentication/LoginComponent';
import history from './helper/History';
import UserProfileComponent from './components/user_profile/UserProfileComponent';
import LogoutComponent from './components/authentication/LogoutComponent';

interface AppState {
  loading: boolean
  successfullyLoaded: boolean
}

const initialState = {
  loading: true,
  successfullyLoaded: false,
};

class App extends React.PureComponent<ReduxState, AppState> {
  constructor(props: ReduxState) {
    super(props);

    this.state = initialState;
  }

  componentDidMount() {
    Fetch.getBasicUrls(this.requestSuccessful, this.requestError);
  }

  private requestSuccessful = (serverResponse: MasonDoc) => {
    const allMoviesUrl = serverResponse['@controls']['moviereviewmeta:movies-all']?.href;
    const allUsersUrl = serverResponse['@controls']['moviereviewmeta:users-all']?.href;
    const allCategoriesUrl = serverResponse['@controls']['moviereviewmeta:categories-all']?.href;

    const addMovieUrl = serverResponse['@controls']['moviereviewmeta:add-movie']?.href;
    const addUserUrl = serverResponse['@controls']['moviereviewmeta:add-user']?.href;
    const addCategoryUrl = serverResponse['@controls']['moviereviewmeta:add-category']?.href;

    const loginUrl = serverResponse['@controls']['moviereviewmeta:login']?.href;
    const currentUserUrl = serverResponse['@controls']['moviereviewmeta:current-user']?.href;

    this.props.appStateDispatch({ type: SET_ALL_MOVIES_URL, value: allMoviesUrl });
    this.props.appStateDispatch({ type: SET_ALL_USERS_URL, value: allUsersUrl });
    this.props.appStateDispatch({ type: SET_ALL_CATEGORIES_URL, value: allCategoriesUrl });
    this.props.appStateDispatch({ type: SET_ADD_MOVIE_URL, value: addMovieUrl });
    this.props.appStateDispatch({ type: SET_ADD_USER_URL, value: addUserUrl });
    this.props.appStateDispatch({ type: SET_ADD_CATEGORY_URL, value: addCategoryUrl });
    this.props.appStateDispatch({ type: SET_LOGIN_URL, value: loginUrl });
    this.props.appStateDispatch({ type: SET_CURRENT_USER_URL, value: currentUserUrl });

    this.setState({
      loading: false,
      successfullyLoaded: true,
    });
  };

  private requestError = () => {
    this.setState({
      loading: false,
    });
  };

  render() {
    if (this.state.loading) {
      return (
        <div className="app-loading">
          <Spinner animation="border" role="status">
            <span className="visually-hidden">Loading...</span>
          </Spinner>
          &nbsp;
          Loading...
        </div>
      );
    }

    if (!this.state.successfullyLoaded) {
      return (
        <div
          className="app-loading-error"
        >
          The API is currently unavailable. Please try again later!
        </div>
      );
    }

    return (
      <HistoryRouter history={history}>
        <Routes>
          <Route
            path="/"
            element={(<MovieListComponent />)}
          />
          <Route
            path="/login"
            element={<LoginComponent />}
          />
          <Route
            path="/logout"
            element={<LogoutComponent />}
          />
          <Route
            path="/movie/:movieId"
            element={<MovieDetailComponent />}
          />
          <Route
            path="/profile"
            element={<UserProfileComponent />}
          />
          <Route
            path="*"
            element={<Navigate to="/" />}
          />
        </Routes>
      </HistoryRouter>
    );
  }
}

export default withAppState(App);
