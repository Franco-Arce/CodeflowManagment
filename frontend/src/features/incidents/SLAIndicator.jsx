import React, { useEffect, useState } from 'react';
import { cn } from '../../lib/utils';

const SLA_HOURS = {
    critical: 4,
    high: 8,
    medium: 24,
    low: 48,
};

export function SLAIndicator({ createdAt, severity, status }) {
    const [timeLeft, setTimeLeft] = useState('');
    const [isBreached, setIsBreached] = useState(false);

    useEffect(() => {
        if (status === 'resolved') {
            setTimeLeft('Resolved');
            return;
        }

        const calculateTimeLeft = () => {
            const created = new Date(createdAt);
            const slaHours = SLA_HOURS[severity.toLowerCase()] || 24;
            const deadline = new Date(created.getTime() + slaHours * 60 * 60 * 1000);
            const now = new Date();
            const diff = deadline - now;

            if (diff <= 0) {
                setIsBreached(true);
                setTimeLeft('Breached');
            } else {
                const hours = Math.floor(diff / (1000 * 60 * 60));
                const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
                setTimeLeft(`${hours}h ${minutes}m`);
            }
        };

        calculateTimeLeft();
        const interval = setInterval(calculateTimeLeft, 60000); // Update every minute

        return () => clearInterval(interval);
    }, [createdAt, severity, status]);

    return (
        <span
            className={cn(
                "inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium",
                status === 'resolved' ? "bg-green-100 text-green-800" :
                    isBreached ? "bg-red-100 text-red-800" : "bg-yellow-100 text-yellow-800"
            )}
        >
            {timeLeft}
        </span>
    );
}
