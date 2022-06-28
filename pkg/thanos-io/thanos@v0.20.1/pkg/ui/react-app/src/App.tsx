import React, { FC } from 'react';
import { Container } from 'reactstrap';
import { Router, Redirect, globalHistory } from '@reach/router';
import { QueryParamProvider } from 'use-query-params';

import { Alerts, Config, Flags, Rules, ServiceDiscovery, Status, Targets, TSDBStatus, PanelList, NotFound } from './pages';
import PathPrefixProps from './types/PathPrefixProps';
import ThanosComponentProps from './thanos/types/ThanosComponentProps';
import Navigation from './thanos/Navbar';
import { Stores, ErrorBoundary, Blocks } from './thanos/pages';

import './App.css';

const defaultRouteConfig: { [component: string]: string } = {
  query: '/graph',
  rule: '/alerts',
  bucket: '/blocks',
  compact: '/loaded',
  store: '/loaded',
};

const App: FC<PathPrefixProps & ThanosComponentProps> = ({ pathPrefix, thanosComponent }) => {
  return (
    <ErrorBoundary>
      <Navigation
        pathPrefix={pathPrefix}
        thanosComponent={thanosComponent}
        defaultRoute={defaultRouteConfig[thanosComponent]}
      />
      <Container fluid style={{ paddingTop: 70 }}>
        <QueryParamProvider reachHistory={globalHistory}>
          <Router basepath={`${pathPrefix}`}>
            <Redirect from="/" to={`${pathPrefix}${defaultRouteConfig[thanosComponent]}`} />

            <PanelList path="/graph" pathPrefix={pathPrefix} />
            <Alerts path="/alerts" pathPrefix={pathPrefix} />
            <Config path="/config" pathPrefix={pathPrefix} />
            <Flags path="/flags" pathPrefix={pathPrefix} />
            <Rules path="/rules" pathPrefix={pathPrefix} />
            <ServiceDiscovery path="/service-discovery" pathPrefix={pathPrefix} />
            <Status path="/status" pathPrefix={pathPrefix} />
            <TSDBStatus path="/tsdb-status" pathPrefix={pathPrefix} />
            <Targets path="/targets" pathPrefix={pathPrefix} />
            <Stores path="/stores" pathPrefix={pathPrefix} />
            <Blocks path="/blocks" pathPrefix={pathPrefix} />
            <Blocks path="/loaded" pathPrefix={pathPrefix} view="loaded" />
            <NotFound pathPrefix={pathPrefix} default defaultRoute={defaultRouteConfig[thanosComponent]} />
          </Router>
        </QueryParamProvider>
      </Container>
    </ErrorBoundary>
  );
};

export default App;
