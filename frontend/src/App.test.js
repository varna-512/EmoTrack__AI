import { render, screen } from '@testing-library/react';
import App from './App';

test('renders EmoTrack AI dashboard shell', () => {
  render(<App />);
  expect(screen.getAllByText(/EmoTrack AI/i).length).toBeGreaterThan(0);
  expect(screen.getByText(/Start Assessment/i)).toBeInTheDocument();
});
