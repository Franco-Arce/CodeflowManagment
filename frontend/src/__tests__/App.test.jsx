import { render, screen } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import App from '../App';

describe('App', () => {
    it('renders login page by default', () => {
        render(<App />);
        expect(screen.getByText(/Codeflow Management/i)).toBeInTheDocument();
        expect(screen.getByLabelText(/Username/i)).toBeInTheDocument();
    });
});
