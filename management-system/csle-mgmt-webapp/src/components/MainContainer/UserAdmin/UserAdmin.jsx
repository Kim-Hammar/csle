import { useState, useEffect, useCallback } from 'react';
import PropTypes from 'prop-types';
import './UserAdmin.css';
import { useNavigate } from "react-router-dom";
import toast from 'react-hot-toast';
import {
    Button,
    OverlayTrigger,
    Tooltip,
    Spinner,
    Table,
    Form
} from 'react-bootstrap';

import {
    API_BASE_URL,
    HTTP_REST_GET,
    HTTP_REST_PUT,
    LOGIN_PAGE_RESOURCE,
    TOKEN_QUERY_PARAM,
    USERS_RESOURCE
} from "../../Common/constants";

/**
 * Component representing the /user-admin-page
 */
const UserAdmin = ({ setSessionData, sessionData }) => {
    const [users, setUsers] = useState([]);
    const [loading, setLoading] = useState(true);
    const [editId, setEditId] = useState(null);
    const [editFormData, setEditFormData] = useState({});
    const navigate = useNavigate();

    const fetchUsers = useCallback(() => {
        fetch(
          `${API_BASE_URL}/${USERS_RESOURCE}`
          + `?${TOKEN_QUERY_PARAM}=${sessionData.token}`,
          {
              method: HTTP_REST_GET,
              headers: new Headers({
                  Accept: "application/vnd.github.cloak-preview"
              })
          }
        )
          .then(res => {
              if (res.status === 401) {
                  toast.error("Session token expired. Please login again.");
                  setSessionData(null);
                  navigate(`/${LOGIN_PAGE_RESOURCE}`);
                  return null;
              }
              return res.json();
          })
          .then(response => {
              if (response) {
                  setUsers(response);
                  setLoading(false);
              }
          })
          .catch(error => console.log("error:" + error));
    }, [navigate, sessionData.token, setSessionData]);

    const refresh = useCallback(() => {
        setLoading(true);
        setEditId(null);
        fetchUsers();
    }, [fetchUsers]);

    const updateUser = useCallback((user) => {
        return fetch(
          `${API_BASE_URL}/${USERS_RESOURCE}/${user.id}`
          + `?${TOKEN_QUERY_PARAM}=${sessionData.token}`,
          {
              method: HTTP_REST_PUT,
              headers: new Headers({
                  Accept: "application/vnd.github.cloak-preview"
              }),
              body: JSON.stringify({ user: user })
          }
        )
          .then(res => {
              if (res.status === 401) {
                  toast.error("Session token expired. Please login again.");
                  setSessionData(null);
                  navigate(`/${LOGIN_PAGE_RESOURCE}`);
                  return null;
              }
              if (res.status === 400) {
                  toast.error("Invalid request, could not update users");
                  return null;
              }
              return res.json();
          })
          .catch(error => console.log("error:" + error));
    }, [navigate, sessionData.token, setSessionData]);

    const handleEditClick = (user) => {
        setEditId(user.id);
        setEditFormData(user);
    };

    const handleEditChange = (e) => {
        const { name, value } = e.target;
        setEditFormData((prev) => ({
            ...prev,
            [name]: value
        }));
    };

    const handleEditSubmit = (e) => {
        e.preventDefault();

        const updatedUsers = users.map((u) =>
          u.id === editId ? editFormData : u
        );
        setUsers(updatedUsers);
        setEditId(null);
    };

    const handleCancelEdit = () => {
        setEditId(null);
    };

    const handleKeyDown = (e) => {
        if (e.key === 'Enter') {
            handleEditSubmit(e);
        }
        if (e.key === 'Escape') {
            handleCancelEdit();
        }
    };

    const saveUsers = () => {
        setLoading(true);
        const updatePromises = users.map(user => updateUser(user));

        Promise.all(updatePromises)
          .then(() => {
              toast.success("All users updated successfully");
              refresh();
          })
          .catch(() => {
              toast.error("Some updates failed");
              setLoading(false);
          });
    };

    useEffect(() => {
        setLoading(true);
        fetchUsers();
    }, [fetchUsers]);

    const renderRefreshTooltip = (props) => (
      <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
          Reload simulations from the backend
      </Tooltip>
    );

    return (
      <div className="Admin">
          <h3> User administration (Click a row to edit, Enter to confirm local change, Save to persist)
              <Button
                variant="primary"
                size="sm"
                className="saveUsersBtn ms-2"
                onClick={saveUsers}
                disabled={loading}
              >
                  {loading ? 'Saving...' : 'Save All Changes'}
              </Button>
          </h3>

          <div className="row">
              <div className="col-sm-1"></div>
              <div className="col-sm-10">

                  {/* Loading Spinner */}
                  {loading && (
                    <div>
                        <span className="spinnerLabel"> Fetching users... </span>
                        <Spinner animation="border" role="status" className="dropdownSpinner">
                            <span className="visually-hidden">Loading...</span>
                        </Spinner>
                    </div>
                  )}

                  {/* Empty State */}
                  {!loading && users.length === 0 && (
                    <div>
                        <span className="emptyText">No users are available</span>
                        <OverlayTrigger
                          placement="top"
                          delay={{ show: 0, hide: 0 }}
                          overlay={renderRefreshTooltip}
                        >
                            <Button variant="button" onClick={refresh}>
                                <i className="fa fa-refresh refreshButton" aria-hidden="true" />
                            </Button>
                        </OverlayTrigger>
                    </div>
                  )}

                  {/* Custom Table */}
                  {!loading && users.length > 0 && (
                    <div className="usersTable table-responsive">
                        <Table striped bordered hover>
                            <thead>
                            <tr>
                                <th>ID</th>
                                <th>Username</th>
                                <th>First Name</th>
                                <th>Last Name</th>
                                <th>E-mail</th>
                                <th>Organization</th>
                                <th>Admin</th>
                                <th>Password</th>
                                <th style={{width: '80px'}}>Edit</th>
                            </tr>
                            </thead>
                            <tbody>
                            {users.map((user) => (
                              <tr key={user.id} onKeyDown={editId === user.id ? handleKeyDown : null}>
                                  {/* ID (Read Only) */}
                                  <td>{user.id}</td>

                                  {/* Editable Columns */}
                                  {editId === user.id ? (
                                    <>
                                        <td><Form.Control size="sm" name="username" value={editFormData.username} onChange={handleEditChange} /></td>
                                        <td><Form.Control size="sm" name="first_name" value={editFormData.first_name} onChange={handleEditChange} /></td>
                                        <td><Form.Control size="sm" name="last_name" value={editFormData.last_name} onChange={handleEditChange} /></td>
                                        <td><Form.Control size="sm" name="email" value={editFormData.email} onChange={handleEditChange} /></td>
                                        <td><Form.Control size="sm" name="organization" value={editFormData.organization} onChange={handleEditChange} /></td>
                                        <td>
                                            <Form.Select size="sm" name="admin" value={editFormData.admin} onChange={handleEditChange}>
                                                <option value="true">true</option>
                                                <option value="false">false</option>
                                            </Form.Select>
                                        </td>
                                        <td><Form.Control size="sm" name="password" value={editFormData.password} onChange={handleEditChange} /></td>
                                        <td>
                                            <Button variant="success" size="sm" onClick={handleEditSubmit}>Ok</Button>
                                        </td>
                                    </>
                                  ) : (
                                    /* Read Only Mode */
                                    <>
                                        <td onClick={() => handleEditClick(user)}>{user.username}</td>
                                        <td onClick={() => handleEditClick(user)}>{user.first_name}</td>
                                        <td onClick={() => handleEditClick(user)}>{user.last_name}</td>
                                        <td onClick={() => handleEditClick(user)}>{user.email}</td>
                                        <td onClick={() => handleEditClick(user)}>{user.organization}</td>
                                        <td onClick={() => handleEditClick(user)}>{String(user.admin)}</td>
                                        <td onClick={() => handleEditClick(user)}>********</td>
                                        <td>
                                            <Button variant="outline-primary" size="sm" onClick={() => handleEditClick(user)}>
                                                Edit
                                            </Button>
                                        </td>
                                    </>
                                  )}
                              </tr>
                            ))}
                            </tbody>
                        </Table>
                    </div>
                  )}

              </div>
              <div className="col-sm-1"></div>
          </div>
      </div>
    );
}

UserAdmin.propTypes = {
    setSessionData: PropTypes.func.isRequired,
    sessionData: PropTypes.object.isRequired
};

export default UserAdmin;