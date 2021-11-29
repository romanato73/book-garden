import { BookTitle } from "../../Components/BookTitle/BookTitle";
import { Breadcrumb } from "../../Components/Ui/Breadcrumb";
import { useEffect, useState } from "react";
import axios from "axios";
import { createAPI } from "../../api";
import { useParams } from "react-router-dom";

const BookTitleShowModule = () => {
  const [bookTitle, setBookTitle] = useState({});
  const [libraries, setLibraries] = useState([]);

  const { id } = useParams();

  useEffect(() => {
    axios
      .get(createAPI("booktitle/:id", { id }))
      .then((response) => setBookTitle(response.data.data))
      .catch((error) => console.log(error));
  }, [id]);

  const items = [
    {
      name: "Book Titles",
      url: "/book-titles",
    },
    {
      name: bookTitle.name?.substr(0, 15) + "...",
      url: `/book-titles/${bookTitle.id}`,
      active: true,
    },
  ];

  return (
    <>
      <Breadcrumb backLink="/book-titles" items={items} />
      <BookTitle bookTitle={bookTitle} />
    </>
  );
};

export default BookTitleShowModule;