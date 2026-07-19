// =======================================
// Institute Location (Currently your home/testing location)
// =======================================

const INSTITUTE_LAT = 17.487024525023813;
const INSTITUTE_LON = 78.39528365316245;

// Allowed distance in meters
const ALLOWED_DISTANCE = 50;


// =======================================
// Calculate Distance (Haversine Formula)
// =======================================

function calculateDistance(lat1, lon1, lat2, lon2) {

    const R = 6371000;

    const dLat = (lat2 - lat1) * Math.PI / 180;
    const dLon = (lon2 - lon1) * Math.PI / 180;

    const a =
        Math.sin(dLat / 2) * Math.sin(dLat / 2) +
        Math.cos(lat1 * Math.PI / 180) *
        Math.cos(lat2 * Math.PI / 180) *
        Math.sin(dLon / 2) *
        Math.sin(dLon / 2);

    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));

    return R * c;

}


// =======================================
// Get Current Location
// =======================================

function verifyLocation(callback) {

    if (!navigator.geolocation) {

        alert("Geolocation is not supported.");

        return;

    }

    navigator.geolocation.getCurrentPosition(

        function(position) {

            const latitude = position.coords.latitude;
            const longitude = position.coords.longitude;

            const distance = calculateDistance(

                latitude,
                longitude,
                INSTITUTE_LAT,
                INSTITUTE_LON

            );

            console.log("Distance :", distance);

            if (distance <= ALLOWED_DISTANCE) {

                callback(true, latitude, longitude);

            }

            else {

                callback(false, latitude, longitude);

            }

        },

        function(error) {

            alert("Location Permission Required");

        },

        {

            enableHighAccuracy: true,
            timeout: 10000,
            maximumAge: 0

        }

    );

}