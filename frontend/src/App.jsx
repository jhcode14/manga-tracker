import "./App.css";
import ActionBar from "./components/ActionBar";
import MangaList from "./components/MangaList";

function App() {
  return (
    <>
      <div>
        <img src="/436774.svg" alt="logo"></img>
      </div>
      <h1>Manga Tracker</h1>
      <ActionBar />
      <MangaList />
    </>
  );
}

export default App;
