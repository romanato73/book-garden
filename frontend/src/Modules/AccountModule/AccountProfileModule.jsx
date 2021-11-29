import { SaveIcon, UserIcon } from "@heroicons/react/outline";
import FormControl from "../../Components/Forms/FormControl";
import { Button } from "../../Components/Ui/Button";
import auth from "../../auth";
import axios from "axios";
import { createAPI } from "../../api";
import qs from "querystring";
import { useState } from "react";
import { Alert } from "../../Components/Ui/Alert";

const AccountProfileModule = () => {
  const [alert, setAlert] = useState(null);

  return (
    <div className="Content">
      <div className="flex flex-col lg:flex-row items-center">
        <div className="w-full lg:w-6/12 mb-8 lg:mb-0">
          <UserIcon className="mx-auto h-32 bg-indigo-600 text-white rounded-full p-4" />
          <div className="my-4 text-2xl text-center font-bold">
            {auth.username}
          </div>
          <div className="italic text-center">{auth.profiledesc}</div>
        </div>
        <form
          method="post"
          className="w-full lg:w-6/12"
          onSubmit={(e) => {
            e.preventDefault();
            const form = new FormData(e.target);
            const data = {};
            for (let pair of form.entries()) {
              data[pair[0]] = pair[1];
            }

            axios
              .put(
                createAPI("person/:id", { id: auth.id }),
                qs.stringify({ ...data })
              )
              .then((response) => {
                if (response.data.status === "success") {
                  // Edited
                  window.scrollTo(0, 0);
                  setAlert({
                    message: "Profile Edited Successfully",
                    type: "success",
                  });
                } else {
                  // Error
                  window.scrollTo(0, 0);
                  setAlert({
                    message: response.data.message,
                    type: "danger",
                  });
                }
              })
              .catch((error) => console.log(error));
          }}
        >
          {alert && (
            <Alert
              message={alert.message}
              type={alert.type}
              onClick={() => setAlert(null)}
            />
          )}

          <h1 className="Content-Title">Account Information</h1>
          <FormControl
            type="text"
            id="name"
            name="name"
            label="First Name"
            value={auth.name}
            placeholder="Joe"
          />
          <FormControl
            type="text"
            id="last_name"
            label="Last Name"
            value={auth.surname}
            placeholder="Doe"
          />
          <FormControl
            type="email"
            id="email"
            label="E-Mail"
            value={auth.email}
            placeholder="user@example.com"
          />
          <hr className="my-4" />
          <h1 className="Content-Title">Change Password</h1>
          <FormControl
            type="password"
            id="password"
            name="password"
            label="Password"
            value={auth.password}
            placeholder="New Password"
          />

          <div className="flex flex-end">
            <Button
              type="submit"
              text="Save"
              variant="primary"
              className="ml-auto"
              icon={<SaveIcon className="h-6 mr-1" />}
            />
          </div>
        </form>
      </div>
    </div>
  );
};

export default AccountProfileModule;