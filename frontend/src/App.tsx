import "./App.css";
import { LatestGames } from "./components/LatestGames";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";

const queryClient = new QueryClient();
function App() {
  return (
    <>
      <QueryClientProvider client={queryClient}>
        <LatestGames />
      </QueryClientProvider>
    </>
  );
}

export default App;
