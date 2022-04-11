import React, { PureComponent } from 'react';
import withRouter from '../helper/RouterHelper';
import HeaderComponent from './HeaderComponent';
import MovieDetailInformationComponent from './MovieDetailInformationComponent';
import MovieDetailReviewsComponent from './MovieDetailReviewsComponent';
import FooterComponent from './FooterComponent';
import { Movie } from '../models/Movie';
import Fetch from '../helper/Fetch';
import { HttpError } from '../models/HttpError';

import './MovieDetailComponent.scss';

type MovieDetailComponentProps = {
  location: {
    state: {
      movieRequestUrl: string
      categoryTitle: string
    }
  }
}

interface MovieDetailComponentState {
  movie?: Movie
  isLoaded: boolean,
}

class MovieDetailComponent
  extends PureComponent <MovieDetailComponentProps, MovieDetailComponentState> {
  constructor(props: MovieDetailComponentProps) {
    super(props);

    this.state = {
      isLoaded: false,
    };
  }

  componentDidMount() {
    this.fetchMovie();
  }

  requestResponseHandler = (serverResponse: Movie) => {
    this.setState({
      movie: serverResponse ?? [],
      isLoaded: true,
    });
  };

  requestErrorHandler = (serverResponse: HttpError) => {
    this.setState({
      isLoaded: true,
    });
  };

  fetchMovie() {
    Fetch.getRequest(
      this.props.location.state.movieRequestUrl,
      this.requestResponseHandler,
      this.requestErrorHandler,
    );
  }

  render() {
    return (
      <div className="movie-item">
        <HeaderComponent pageTitle={this.state.movie?.title ?? 'Movie Item'} />
        <div className="main">
          <MovieDetailInformationComponent
            movie={this.state.movie}
            categoryTitle={this.props.location.state.categoryTitle}
          />
          <MovieDetailReviewsComponent
            reviewsUrl={this.state.movie?.['@controls']['moviereviewmeta:reviews-for-movie']?.href}
          />
        </div>
        <FooterComponent />
      </div>
    );
  }
}

export default withRouter(MovieDetailComponent);
