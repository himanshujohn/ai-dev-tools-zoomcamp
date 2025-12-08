import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import App from '../App';

describe('Snake Game App', () => {
  it('renders login form and allows login', async () => {
    render(<App />);
    expect(screen.getByRole('heading', { name: /login/i })).toBeInTheDocument();
    fireEvent.change(screen.getByPlaceholderText(/username/i), { target: { value: 'demo' } });
    fireEvent.change(screen.getByPlaceholderText(/password/i), { target: { value: 'demo' } });
    fireEvent.click(screen.getAllByText('Login').find(el => el.tagName === 'BUTTON'));
    await waitFor(() => expect(screen.getByText(/welcome/i)).toBeInTheDocument());
  });

  it('can sign up and see menu', async () => {
    render(<App />);
    fireEvent.click(screen.getByText(/sign up/i));
    fireEvent.change(screen.getByPlaceholderText(/username/i), { target: { value: 'newuser' } });
    fireEvent.change(screen.getByPlaceholderText(/password/i), { target: { value: 'newpass' } });
    fireEvent.click(screen.getAllByText('Sign Up').find(el => el.tagName === 'BUTTON'));
    await waitFor(() => expect(screen.getByText(/welcome/i)).toBeInTheDocument());
  });

  it('shows leaderboard after login', async () => {
    render(<App />);
    fireEvent.change(screen.getByPlaceholderText(/username/i), { target: { value: 'demo' } });
    fireEvent.change(screen.getByPlaceholderText(/password/i), { target: { value: 'demo' } });
    fireEvent.click(screen.getAllByText('Login').find(el => el.tagName === 'BUTTON'));
    await waitFor(() => expect(screen.getByText(/welcome/i)).toBeInTheDocument());
    fireEvent.click(screen.getByText(/leaderboard/i));
    await waitFor(() => expect(screen.getByText(/leaderboard/i)).toBeInTheDocument());
  });

  it('can watch a game', async () => {
    render(<App />);
    fireEvent.change(screen.getByPlaceholderText(/username/i), { target: { value: 'demo' } });
    fireEvent.change(screen.getByPlaceholderText(/password/i), { target: { value: 'demo' } });
    fireEvent.click(screen.getAllByText('Login').find(el => el.tagName === 'BUTTON'));
    await waitFor(() => expect(screen.getByText(/welcome/i)).toBeInTheDocument());
    fireEvent.click(screen.getByText(/watch players/i));
    await waitFor(() => expect(screen.getByText(/active games/i)).toBeInTheDocument());
    fireEvent.click(screen.getAllByText(/watch/i)[0]);
    await waitFor(() => expect(screen.getByText(/watching/i)).toBeInTheDocument());
  });
});
