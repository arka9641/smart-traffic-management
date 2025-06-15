import React, { useEffect, useState } from 'react';
import { MapContainer, TileLayer, CircleMarker } from 'react-leaflet';

const TrafficMap = () => {
    const [trafficData, setTrafficData] = useState([]);

    useEffect(() => {
        fetch('/api/traffic-data')
            .then(res => res.json())
            .then(data => setTrafficData(data));
    }, []);

    return (
        <MapContainer center={[51.505, -0.09]} zoom={13}>
            <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
            {trafficData.map(sensor => (
                <CircleMarker
                    key={sensor.sensor_id}
                    center={[sensor.lat, sensor.lng]}
                    radius={sensor.vehicle_count / 10}
                    color={sensor.avg_speed < 20 ? 'red' : 'green'}
                />
            ))}
        </MapContainer>
    );
};