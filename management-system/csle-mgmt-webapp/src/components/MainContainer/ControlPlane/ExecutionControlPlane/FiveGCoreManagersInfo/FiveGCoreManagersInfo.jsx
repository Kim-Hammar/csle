import './FiveGCoreManagersInfo.css'
import Card from 'react-bootstrap/Card'
import Button from 'react-bootstrap/Button'
import Table from 'react-bootstrap/Table'
import Collapse from 'react-bootstrap/Collapse'
import SpinnerOrButton from '../SpinnerOrButton/SpinnerOrButton.jsx'
import LogsButton from '../LogsButton/LogsButton.jsx'
import Open5GSImg from './Open5GS.png'
import {
  FIVE_G_CORE_MANAGER_SUBRESOURCE, FIVE_G_CORE_SUBRESOURCE,
  START_ALL_PROPERTY,
  STOP_ALL_PROPERTY
} from '../../../../Common/constants'

/**
 * Subcomponent of the /control-plane page that contains information about 5G core managers
 */
const FiveGCoreManagersInfo = (props) => {

  const renderFiveGCoreTooltip = (props) => {
    return (<Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
      View Ryu&apos;s web interface
    </Tooltip>)
  }

  const FiveGCoreWebButton = (props) => {
    if(props.running && props.port !== -1 && !props.loading) {
      return (
        <OverlayTrigger
          placement="top"
          delay={{show: 0, hide: 0}}
          overlay={renderFiveGCoreTooltip}
        >
          <a href={`${HTTP_PREFIX}${props.ip}:${props.port}`} target="_blank" rel="noopener noreferrer">
            <Button variant="light" className="startButton" size="sm">
              <img src={Open5GSImg} alt="Open5Gs" className="img-fluid elastic"/>
            </Button>
          </a>
        </OverlayTrigger>
      )
    } else {
      return (<></>)
    }
  }

  return (
    <Card className="subCard">
      <Card.Header>
        <Button
          onClick={() => props.setFiveGCoreManagersOpen(!props.fiveGCoreManagersOpen)}
          aria-controls="fiveGCoreManagersBody"
          aria-expanded={props.fiveGCoreManagersOpen}
          variant="link"
        >
          <h5 className="semiTitle"> 5G core managers
            <i className="fa fa-server headerIcon" aria-hidden="true"></i>
          </h5>
        </Button>
      </Card.Header>
      <Collapse in={props.fiveGCoreManagersOpen}>
        <div id="fiveGCoreManagersOpen" className="cardBodyHidden">
          <div className="aggregateActionsContainer">
            <span className="aggregateActions">Stop all managers:</span>
            <SpinnerOrButton
              loading={props.loadingEntities.includes(
                `${FIVE_G_CORE_MANAGER_SUBRESOURCE}-${STOP_ALL_PROPERTY}`)}
              running={true} entity={FIVE_G_CORE_MANAGER_SUBRESOURCE}
              name={STOP_ALL_PROPERTY} ip={STOP_ALL_PROPERTY}
              startOrStop={props.startOrStop}
            />
            <span className="aggregateActions">Start all managers:</span>
            <SpinnerOrButton
              loading={props.loadingEntities.includes(
                `${FIVE_G_CORE_MANAGER_SUBRESOURCE}-${START_ALL_PROPERTY}`)}
              running={false} entity={FIVE_G_CORE_MANAGER_SUBRESOURCE}
              name={START_ALL_PROPERTY} ip={START_ALL_PROPERTY}
              startOrStop={props.startOrStop}
            />
          </div>

          <div className="table-responsive">
            <Table striped bordered hover>
              <thead>
              <tr>
                <th>Service</th>
                <th>IP</th>
                <th>Port</th>
                <th>Status</th>
                <th>Actions</th>
              </tr>
              </thead>
              <tbody>
              {props.fiveGCoreManagersInfo.five_g_core_managers_statuses.map((status, index) =>
                <tr key={`${FIVE_G_CORE_MANAGER_SUBRESOURCE}-${index}`}>
                  <td>5G core manager</td>
                  <td>{props.fiveGCoreManagersInfo.ips[index]}</td>
                  <td>{props.fiveGCoreManagersInfo.ports[index]}</td>
                  {props.activeStatus(props.fiveGCoreManagersInfo.five_g_core_managers_running[index])}
                  <td>
                    <FiveGCoreWebButton
                      loading={props.loadingEntities.includes(
                        `${FIVE_G_CORE_SUBRESOURCE}-`
                        + `${props.fiveGCoreManagersInfo.ips[index]}`)}
                      name={props.fiveGCoreManagersInfo.ips[index]}
                      port={props.fiveGCoreManagersInfo.local_webui_port}
                      running={status.amf_running}
                      ip={props.fiveGCoreManagersInfo.physical_server_ip}
                    />
                    <SpinnerOrButton
                      loading={props.loadingEntities.includes(
                        `${FIVE_G_CORE_MANAGER_SUBRESOURCE}-`
                        + `${props.fiveGCoreManagersInfo.ips[index]}`)}
                      running={props.fiveGCoreManagersInfo.five_g_core_managers_running[index]}
                      entity={FIVE_G_CORE_MANAGER_SUBRESOURCE} name={FIVE_G_CORE_MANAGER_SUBRESOURCE}
                      ip={props.fiveGCoreManagersInfo.ips[index]}
                      startOrStop={props.startOrStop}
                    />
                    <LogsButton name={props.fiveGCoreManagersInfo.ips[index]}
                                entity={FIVE_G_CORE_MANAGER_SUBRESOURCE}
                                getLogs={props.getLogs}
                    />
                  </td>
                </tr>
              )}

              {props.fiveGCoreManagersInfo.five_g_core_managers_statuses.map((status, index) =>
                <tr key={`${FIVE_G_CORE_SUBRESOURCE}-${index}`}>
                  <td>5G core</td>
                  <td>{props.fiveGCoreManagersInfo.ips[index]}</td>
                  <td></td>
                  {props.activeStatus(status.amf_running)}
                  <td>
                    <SpinnerOrButton
                      loading={props.loadingEntities.includes(
                        `${FIVE_G_CORE_SUBRESOURCE}-`
                        + `${props.fiveGCoreManagersInfo.ips[index]}`)}
                      running={status.amf_running}
                      entity={FIVE_G_CORE_SUBRESOURCE}
                      name={FIVE_G_CORE_SUBRESOURCE}
                      ip={props.fiveGCoreManagersInfo.ips[index]}
                      startOrStop={props.startOrStop}
                    />
                    <LogsButton name={props.fiveGCoreManagersInfo.ips[index]}
                                entity={FIVE_G_CORE_SUBRESOURCE}
                                getLogs={props.getLogs}
                    />
                  </td>
                </tr>
              )}
              </tbody>
            </Table>
          </div>
        </div>
      </Collapse>
    </Card>
  )

}

FiveGCoreManagersInfo.propTypes = {}
FiveGCoreManagersInfo.defaultProps = {}
export default FiveGCoreManagersInfo
