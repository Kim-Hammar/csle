import { useState, useEffect, useCallback } from 'react'
import './SystemAdmin.css'
import { useNavigate } from 'react-router-dom'
import toast from 'react-hot-toast'
import {
  Button,
  OverlayTrigger,
  Tooltip,
  Spinner,
  Table,
  Form
} from 'react-bootstrap'
import {
  API_BASE_URL,
  HTTP_REST_GET,
  HTTP_REST_PUT,
  CONFIG_RESOURCE,
  TOKEN_QUERY_PARAM,
  LOGIN_PAGE_RESOURCE
} from '../../Common/constants'


/**
 * Component representing the /system-admin-page
 */
const SystemAdmin = ({ setSessionData, sessionData }) => {
  const [parametersConfig, setParametersConfig] = useState([])
  const [clusterConfig, setClusterConfig] = useState([])
  const [loading, setLoading] = useState(true)
  const [editParamKey, setEditParamKey] = useState(null)
  const [tempParamValue, setTempParamValue] = useState('')
  const [editClusterKey, setEditClusterKey] = useState(null)
  const [tempClusterData, setTempClusterData] = useState({})
  const navigate = useNavigate()

  const fetchConfig = useCallback(() => {
    fetch(
      `${API_BASE_URL}/${CONFIG_RESOURCE}`
      + `?${TOKEN_QUERY_PARAM}=${sessionData.token}`,
      {
        method: HTTP_REST_GET,
        headers: new Headers({
          Accept: 'application/vnd.github.cloak-preview'
        })
      }
    )
      .then(res => {
        if (res.status === 401) {
          toast.error('Session token expired. Please login again.')
          setSessionData(null)
          navigate(`/${LOGIN_PAGE_RESOURCE}`)
          return null
        }
        return res.json()
      })
      .then(response => {
        if (response) {
          setParametersConfig(response.parameters || [])
          // Guard against missing cluster_config
          if (response.cluster_config && response.cluster_config.cluster_nodes) {
            setClusterConfig(response.cluster_config.cluster_nodes)
          }
          setLoading(false)
        }
      })
      .catch(error => console.log('error:' + error))
  }, [navigate, sessionData.token, setSessionData])

  const refresh = useCallback(() => {
    setLoading(true)
    setEditParamKey(null)
    setEditClusterKey(null)
    fetchConfig()
  }, [fetchConfig])

  const updateConfig = useCallback((configObj) => {
    fetch(
      `${API_BASE_URL}/${CONFIG_RESOURCE}`
      + `?${TOKEN_QUERY_PARAM}=${sessionData.token}`,
      {
        method: HTTP_REST_PUT,
        headers: new Headers({
          Accept: 'application/vnd.github.cloak-preview'
        }),
        body: JSON.stringify({ config: configObj })
      }
    )
      .then(res => {
        if (res.status === 401) {
          toast.error('Session token expired. Please login again.')
          setSessionData(null)
          navigate(`/${LOGIN_PAGE_RESOURCE}`)
          return null
        }
        if (res.status === 400) {
          toast.error('Invalid request, could not update configuration')
          return null
        }
        return res.json()
      })
      .then(() => {
        toast.success('Configuration saved successfully')
        refresh()
      })
      .catch(error => console.log('error:' + error))
  }, [navigate, refresh, sessionData.token, setSessionData])

  const handleParamEditStart = (row) => {
    setEditParamKey(row.param)
    setTempParamValue(row.value)
  }

  const handleParamSaveLocal = () => {
    const updatedParams = parametersConfig.map(p =>
      p.param === editParamKey ? { ...p, value: tempParamValue } : p
    )
    setParametersConfig(updatedParams)
    setEditParamKey(null)
  }

  const handleClusterEditStart = (row) => {
    setEditClusterKey(row.ip)
    setTempClusterData({ ...row })
  }

  const handleClusterChange = (e) => {
    const { name, value } = e.target
    const finalValue = name === 'leader' ? (value === 'true') : value

    setTempClusterData(prev => ({
      ...prev,
      [name]: finalValue
    }))
  }

  const handleClusterSaveLocal = () => {
    const updatedCluster = clusterConfig.map(node =>
      node.ip === editClusterKey ? tempClusterData : node
    )
    setClusterConfig(updatedCluster)
    setEditClusterKey(null)
  }

  const saveConfig = () => {
    var clusterConfigObj = {
      'cluster_nodes': clusterConfig
    }
    var configObj = {}
    configObj['cluster_config'] = clusterConfigObj
    configObj['parameters'] = parametersConfig

    updateConfig(configObj)
  }

  const handleKeyDown = (e, saveFunc, cancelFunc) => {
    if (e.key === 'Enter') {
      e.preventDefault()
      saveFunc()
    }
    if (e.key === 'Escape') {
      cancelFunc()
    }
  }

  useEffect(() => {
    setLoading(true)
    fetchConfig()
  }, [fetchConfig])

  const renderRefreshTooltip = (props) => (
    <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
      Reload configuration from backend
    </Tooltip>
  )

  return (
    <div className="Admin">
      <h3> System Configuration (Click value to edit, Enter to confirm, Save to persist)
        <Button className="btn btn-primary btn-sm saveUsersBtn ms-2" onClick={saveConfig}>
          Save All
        </Button>
      </h3>
      <div className="row">
        <div className="col-sm-1"></div>
        <div className="col-sm-10">
          {loading ? (
            <div className="text-center">
              <span className="spinnerLabel"> Fetching configuration... </span>
              <Spinner animation="border" role="status" size="sm" />
            </div>
          ) : (
            <div className="configTable table-responsive">
              {parametersConfig.length === 0 ? (
                <div className="emptyText">No parameters available</div>
              ) : (
                <Table striped bordered hover>
                  <thead>
                  <tr>
                    <th>Parameter</th>
                    <th>Value</th>
                    <th style={{ width: '100px' }}>Action</th>
                  </tr>
                  </thead>
                  <tbody>
                  {parametersConfig.map((row) => (
                    <tr key={row.param}>
                      <td>{row.param}</td>
                      <td>
                        {editParamKey === row.param ? (
                          <Form.Control
                            type="text"
                            size="sm"
                            value={tempParamValue}
                            onChange={(e) => setTempParamValue(e.target.value)}
                            onKeyDown={(e) => handleKeyDown(e, handleParamSaveLocal, () => setEditParamKey(null))}
                            autoFocus
                          />
                        ) : (
                          <span onClick={() => handleParamEditStart(row)}
                                style={{ cursor: 'pointer', display: 'block', minHeight: '20px' }}>
                                                            {row.value}
                                                        </span>
                        )}
                      </td>
                      <td>
                        {editParamKey === row.param ? (
                          <Button variant="success" size="sm" onClick={handleParamSaveLocal}>OK</Button>
                        ) : (
                          <Button variant="outline-primary" size="sm"
                                  onClick={() => handleParamEditStart(row)}>Edit</Button>
                        )}
                      </td>
                    </tr>
                  ))}
                  </tbody>
                </Table>
              )}
            </div>
          )}
        </div>
        <div className="col-sm-1"></div>
      </div>

      <h3 className="mt-4"> Cluster Configuration (Click value to edit, Enter to confirm)
        <Button className="btn btn-primary btn-sm saveUsersBtn ms-2" onClick={saveConfig}>
          Save All
        </Button>
      </h3>
      <div className="row">
        <div className="col-sm-1"></div>
        <div className="col-sm-10">
          {loading ? (
            <div className="text-center"><Spinner animation="border" size="sm" /></div>
          ) : (
            <div className="configTable table-responsive">
              {clusterConfig.length === 0 ? (
                <div>
                  <span className="emptyText">No cluster configuration available</span>
                  <OverlayTrigger placement="top" overlay={renderRefreshTooltip}>
                    <Button variant="link" onClick={refresh}><i className="fa fa-refresh" /></Button>
                  </OverlayTrigger>
                </div>
              ) : (
                <Table striped bordered hover>
                  <thead>
                  <tr>
                    <th>IP</th>
                    <th>Leader</th>
                    <th style={{ width: '100px' }}>Action</th>
                  </tr>
                  </thead>
                  <tbody>
                  {clusterConfig.map((row) => (
                    <tr key={row.ip}>
                      <td>{row.ip}</td>
                      <td>
                        {editClusterKey === row.ip ? (
                          <Form.Control
                            as="select"
                            size="sm"
                            name="leader"
                            value={String(tempClusterData.leader)}
                            onChange={handleClusterChange}
                            onKeyDown={(e) => handleKeyDown(e, handleClusterSaveLocal, () => setEditClusterKey(null))}
                          >
                            <option value="true">true</option>
                            <option value="false">false</option>
                          </Form.Control>
                        ) : (
                          <span onClick={() => handleClusterEditStart(row)}
                                style={{ cursor: 'pointer', display: 'block' }}>
                                                            {String(row.leader)}
                                                        </span>
                        )}
                      </td>
                      <td>
                        {editClusterKey === row.ip ? (
                          <Button variant="success" size="sm" onClick={handleClusterSaveLocal}>OK</Button>
                        ) : (
                          <Button variant="outline-primary" size="sm"
                                  onClick={() => handleClusterEditStart(row)}>Edit</Button>
                        )}
                      </td>
                    </tr>
                  ))}
                  </tbody>
                </Table>
              )}
            </div>
          )}
        </div>
        <div className="col-sm-1"></div>
      </div>
    </div>
  )
}

export default SystemAdmin