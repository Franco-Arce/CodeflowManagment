import React from 'react';
import { Button } from '../../components/ui/button';
import { SLAIndicator } from './SLAIndicator';

export function IncidentTable({ incidents, onResolve }) {
    return (
        <div className="w-full overflow-auto rounded-lg border border-slate-200 bg-white shadow-sm">
            <table className="w-full text-sm text-left">
                <thead className="bg-slate-50 text-slate-500 font-medium border-b border-slate-200">
                    <tr>
                        <th className="px-4 py-3">ID</th>
                        <th className="px-4 py-3">Title</th>
                        <th className="px-4 py-3">Severity</th>
                        <th className="px-4 py-3">Status</th>
                        <th className="px-4 py-3">SLA Remaining</th>
                        <th className="px-4 py-3 text-right">Actions</th>
                    </tr>
                </thead>
                <tbody className="divide-y divide-slate-100">
                    {incidents.map((incident) => (
                        <tr key={incident.id} className="hover:bg-slate-50/50 transition-colors">
                            <td className="px-4 py-3 font-medium">#{incident.id}</td>
                            <td className="px-4 py-3">{incident.title}</td>
                            <td className="px-4 py-3">
                                <span className={`capitalize ${incident.severity === 'critical' ? 'text-red-600 font-bold' :
                                        incident.severity === 'high' ? 'text-orange-600' : 'text-slate-600'
                                    }`}>
                                    {incident.severity}
                                </span>
                            </td>
                            <td className="px-4 py-3">
                                <span className={`inline-flex items-center rounded-md px-2 py-1 text-xs font-medium ring-1 ring-inset ${incident.status === 'open' ? 'bg-blue-50 text-blue-700 ring-blue-700/10' :
                                        incident.status === 'resolved' ? 'bg-green-50 text-green-700 ring-green-600/20' :
                                            'bg-gray-50 text-gray-600 ring-gray-500/10'
                                    }`}>
                                    {incident.status}
                                </span>
                            </td>
                            <td className="px-4 py-3">
                                <SLAIndicator
                                    createdAt={incident.created_at}
                                    severity={incident.severity}
                                    status={incident.status}
                                />
                            </td>
                            <td className="px-4 py-3 text-right">
                                {incident.status !== 'resolved' && (
                                    <Button
                                        size="sm"
                                        variant="outline"
                                        onClick={() => onResolve(incident.id)}
                                    >
                                        Resolve
                                    </Button>
                                )}
                            </td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
}
