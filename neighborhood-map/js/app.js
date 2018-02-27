"use strict";

// Global variables
var map, infowindow, marker, placeLat, placeLon, bounds;
var markers = [];

//client id and secret of foursquare
var CLIENT_ID = "K4BZBKUIRUP3Z52BUTPLS3QSKLC01JJOEBYV41B4OGO4QFAC";
var CLIENT_SECRET = "SYZHFSLUOOIXPRKKE3HUW4GOEOZRRPQ1JBTZE1MGJMPQJAC2";

// Constructor for location objects , which we will use to set marker and display names on infowindow and list
var Location = function(initialLocations) {
  this.name = initialLocations.venue.name;
  this.address = initialLocations.venue.location.address;
  this.url  = initialLocations.venue.url;
  this.lat  = initialLocations.venue.location.lat;
  this.lng  = initialLocations.venue.location.lng;
  this.icon = initialLocations.icon;
};

function googleError() {
    alert('Google Maps did not load. That\'s an error. Please refresh the page and try again!');
};


//callback function after map initialize
function initMap() {
    //initialize the map with default zoom and center point
    map = new google.maps.Map(document.getElementById('map'), {
        center: new google.maps.LatLng(47.809490, 13.055010), // shows the city center of Salzburg, Austria
        zoom: 13
      });

    //call knockout model
    ko.applyBindings(new ViewModel()); // Apply Bindings from the ViewModel
  }
  var ViewModel = function() {
    var app = this;

    app.ErrorText = ko.observable();
    app.errorHandler = function (jqXHR, textStatus, errorThrown) {
        app.ErrorText('An error has occured. Please refresh the page and try again in a little while. (' + textStatus + ':' + errorThrown + ')');
    };
    app.validationErrorHandler = function (err) {
        //todo
        alert('Validation error: ' + err);
    }

    ko.bindingProvider.instance = new function() {
        var original = new ko.bindingProvider();

        //determine if an element has any bindings
        this.nodeHasBindings = original.nodeHasBindings;

        //return the bindings given a node and the bindingContext
        this.getBindings = function(node, bindingContext) {
            var result;
            try {
                result = original.getBindings(node, bindingContext);
            }
            catch (e) {
                if (console && console.log) {
                    app.ErrorText('An error has occured, please refresh the page and try again in a little while.');
                }
            }

            return result;
        };
    };

    var service;
    var defaultNeighborhood = 'Salzburg'; // the city for which neighborhoods will be taken from foursquare api
    app.LocationList = ko.observableArray([]);
    // Markers array.
    app.LocationMarker = ko.observableArray();
    // Track user input and apply filter.
    app.searchText = ko.observable();

    app.LocationInfo = ko.observable();


    function initializeNeighborhood(neighborhood) {
      getNeighborhood(neighborhood);
    }

    function getNeighborhood(neighborhood) {

      // the search request object
      var request = {
        query: neighborhood
      };

      // creates a Google place search service object.
      // PlacesService does the work of searching for location data.
      service = new google.maps.places.PlacesService(map);
      // searches the Google Maps API for location data and runs the callback
      // function with the search results after each search.
      service.textSearch(request, getNeighborhoodCallback);
    }

    function getNeighborhoodCallback(results, status) {
      if (status == google.maps.places.PlacesServiceStatus.OK) {
        getNeighborhoodVenues(results[0]);
      }
    }

    function getNeighborhoodVenues(place) {
      var placeLat = place.geometry.location.lat();
      var placeLon = place.geometry.location.lng();

      var foursquareBaseURL = 'https://api.foursquare.com/v2/venues/explore?';
      var foursquareID = 'client_id='+CLIENT_ID+'&client_secret='+CLIENT_SECRET;
      var neighborhoodLL = '&ll=' + placeLat + ',' + placeLon;
      var query = '&query=';
      var foursquareURL = foursquareBaseURL + foursquareID + '&v=20130815&venuePhotos=1' + neighborhoodLL + query;

      $.ajax({
        url: foursquareURL,
        async: true,
        success: function(data) {

          var initialFoursquareData = data.response.groups[0].items;

              // retrieve and set foursquare venue data in topPicks observable array
              initialFoursquareData.forEach(function(venueItem) {

                //self.topPicks.push( new Venue(venueItem, foursquareID) );

                app.LocationList.push(new Location(venueItem));
              });

              // set bounds according to suggestedBounds from foursquare data resonse
              var tempBounds = data.response.suggestedBounds;


              if (tempBounds != undefined) {
                bounds = new google.maps.LatLngBounds(
                  new google.maps.LatLng(tempBounds.sw.lat, tempBounds.sw.lng),
                  new google.maps.LatLng(tempBounds.ne.lat, tempBounds.ne.lng));
                map.fitBounds(bounds);
              }

              infowindow = new google.maps.InfoWindow();

              app.LocationList().forEach(function(LocationElem) {
                  // Each Location gets a marker object.
                  marker = new google.maps.Marker({
                    position: new google.maps.LatLng(LocationElem.lat, LocationElem.lng),
                    map: map,
                    icon: LocationElem.icon,
                    animation: google.maps.Animation.DROP
                  });

                  //Connect list with map markers.
                  LocationElem.marker = marker;

                  google.maps.event.addListener(marker, 'click', function() {
                      infowindow.open(map, this); // Shows InfoWindow of exactly this location.
                      // center position on click
                      map.panTo(LocationElem.marker.getPosition());
                      // animate marker
                      LocationElem.marker.setAnimation(google.maps.Animation.BOUNCE);
                      setTimeout(function() {
                        LocationElem.marker.setAnimation(null);
                      }, 1400); // x * 700 = the perfect bounce

                      //get specific location details with help of foursquare api
                      var foursquareUrl = 'https://api.foursquare.com/v2/venues/search?client_id=' + CLIENT_ID + '&client_secret=' + CLIENT_SECRET + '&v=20130815&ll=' + LocationElem.lat  + ',' + LocationElem.lng + '&query=\'' + LocationElem.name + '\'&limit=1';

                      //if success set its content in infowindow
                      $.getJSON(foursquareUrl, function(data){
                        console.log("success");
                      })
                      .done(function(data) {
                        var info = data.response.venues[0];
                        if (typeof info.url === 'undefined') {
                          info.url = "";
                        }

                        info.name = info.name || 'No name provided!';
                        info.location.address = info.location.address || 'No address provided!';

                        var LocationInfo = '<h4>' + info.name + '</h4>' +
                        '<h5>' + info.location.address + '</h5>' +
                        '<a href="' + info.url + '">' + info.url + '</a>';

                        //call foursquare api to get images of venue
                        var foursquareImgUrl = 'https://api.foursquare.com/v2/venues/' + data.response.venues[0].id + '/photos?client_id=' + CLIENT_ID + '&client_secret=' + CLIENT_SECRET + '&v=20130815';

                        infowindow.setContent(LocationInfo);
                        $.getJSON(foursquareImgUrl, function (data) {
                          console.log("success2");
                        })
                        .fail(function(jqXHR, textStatus, errorThrown) {
                          app.errorHandler(null, textStatus, " Could not load all data!");
                        })
                        .done(function(data){
                          var info = data.response.photos.items[0];
                          var width = 150;
                          var height = 150;
                          LocationInfo += '<p><img alt="picture" src="' + info.prefix + width + 'x' + height + info.suffix + '"></p>';
                            //set infowindow with content and images in google map
                            infowindow.setContent(LocationInfo);
                          });
                      })
                      .fail(function (jqXHR, textStatus, errorThrown) {
                        app.errorHandler(null, textStatus, " Could not load all data!");
                      });
                    });
                });

              app.getContent = function(LocationElem) {
                google.maps.event.trigger(LocationElem.marker, 'click');
              };
              // All markers pushed into LocationList array.
              app.LocationList().forEach(function(Location) {
                app.LocationMarker.push(Location);
              });

            },
                  error: function(jqXHR, textStatus, errorThrown) {
              app.errorHandler(null, textStatus, " Error while loading Foursquare data!");
            }
                });


        // Filters locations depending on input in search field

      }
    //Display locations in sidebar and apply filter on serch box
    app.useFilter = function() {
      var searchInput = app.searchText().toLowerCase();
      app.LocationMarker.removeAll();

      app.LocationList().forEach(function(Location) {

        Location.marker.setVisible(false);
            // Dynamic search.
            if (Location.name.toLowerCase().indexOf(searchInput) >= 0) {
              app.LocationMarker.push(Location);
            }
          });
      app.LocationMarker().forEach(function(Location) {
        Location.marker.setVisible(true);
      });
    };

    //initialization of app
    initializeNeighborhood(defaultNeighborhood);
  };
