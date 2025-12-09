import React, { useEffect, useState } from 'react';
import api from '../lib/api';
import { IncidentTable } from '../features/incidents/IncidentTable';
import { Button } from '../components/ui/button';

export default function Incidents() {
    const [incidents, setIncidents] = useState([]);

    const fetchIncidents = async () => {
        try {
            const response = await api.get('/incidents');
            setIncidents(response.data);
        } catch (error) {
            console.error("Failed to fetch incidents", error);
        }
    };

    useEffect(() => {
        fetchIncidents();
    }, []);

    const handleResolve = async (id) => {
        try {
            await api.put(`/incidents/${id}`, { status: 'resolved', resolved_at: new Date().toISOString() });
            fetchIncidents();
        } catch (error) {
            console.error("Failed to resolve incident", error);
        }
    };

    return (
        <div className="space-y-6">
            <div className="flex items-center justify-between">
                <h1 className="text-3xl font-bold tracking-tight">Incidents</h1>
                <Button>Create Incident</Button>
            </div>
            <IncidentTable incidents={incidents} onResolve={handleResolve} />
        </div>
    );
}
