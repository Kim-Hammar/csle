import './App.css'
import MainContainer from './components/MainContainer/MainContainer.jsx'
import NotFound from './components/MainContainer/NotFound/NotFound.jsx'
import Emulations from './components/MainContainer/Emulations/Emulations.jsx'
import Monitoring from './components/MainContainer/Monitoring/Monitoring.jsx'
import Traces from './components/MainContainer/Traces/Traces.jsx'
import EmulationStatistics from './components/MainContainer/EmulationStatistics/EmulationStatistics.jsx'
import SystemModels from './components/MainContainer/SystemModels/SystemModels.jsx'
import PolicyExamination from './components/MainContainer/PolicyExamination/PolicyExamination.jsx'
import ContainerImages from './components/MainContainer/ContainerImages/ContainerImages.jsx'
import Simulations from './components/MainContainer/Simulations/Simulations.jsx'
import TrainingResults from './components/MainContainer/TrainingResults/TrainingResults.jsx'
import About from './components/MainContainer/About/About.jsx'
import UserAdmin from './components/MainContainer/UserAdmin/UserAdmin.jsx'
import SystemAdmin from './components/MainContainer/SystemAdmin/SystemAdmin.jsx'
import LogsAdmin from './components/MainContainer/LogsAdmin/LogsAdmin.jsx'
import Login from './components/MainContainer/Login/Login.jsx'
import Register from './components/MainContainer/Register/Register.jsx'
import Policies from './components/MainContainer/Policies/Policies.jsx'
import Jobs from './components/MainContainer/Jobs/Jobs.jsx'
import ControlPlane from './components/MainContainer/ControlPlane/ControlPlane.jsx'
import SDNControllers from './components/MainContainer/SDNControllers/SDNControllers.jsx'
import Downloads from './components/MainContainer/Downloads/Downloads.jsx'
import CreateEmulation from './components/MainContainer/CreateEmulation/CreateEmulation.jsx'
import RecoveryAI from './components/MainContainer/RecoveryAI/RecoveryAI.jsx'
import ServerCluster from './components/MainContainer/ServerCluster/ServerCluster.jsx'
import ContainerTerminal from './components/MainContainer/ContainerTerminal/ContainerTerminal.jsx'
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import useSession from './components/MainContainer/SessionManagement/useSession'
import toast, { Toaster } from 'react-hot-toast'
import {
  LOGIN_PAGE_RESOURCE,
  EMULATIONS_PAGE_RESOURCE,
  SIMULATIONS_PAGE_RESOURCE,
  EMULATION_STATISTICS_PAGE_RESOURCE,
  MONITORING_PAGE_RESOURCE,
  TRACES_PAGE_RESOURCE,
  POLICY_EXAMINATION_PAGE_RESOURCE,
  IMAGES_PAGE_RESOURCE,
  TRAINING_PAGE_RESOURCE,
  POLICIES_PAGE_RESOURCE,
  SDN_CONTROLLERS_PAGE_RESOURCE,
  CONTROL_PLANE_PAGE_RESOURCE,
  CONTAINER_TERMINAL_PAGE_RESOURCE,
  ABOUT_PAGE_RESOURCE,
  DOWNLOADS_PAGE_RESOURCE,
  REGISTER_PAGE_RESOURCE,
  USER_ADMIN_PAGE_RESOURCE,
  SYSTEM_ADMIN_PAGE_RESOURCE,
  LOGS_ADMIN_PAGE_RESOURCE,
  SYSTEM_MODELS_PAGE_RESOURCE,
  JOBS_PAGE_RESOURCE,
  SERVER_CLUSTER_PAGE_RESOURCE,
  CREATE_EMULATION_PAGE_RESOURCE,
  RECOVERY_AI_PAGE_RESOURCE
} from './components/Common/constants'

function App() {
  /**
   * Container component containing the main components of the page and defining the routes
   * @returns {JSX.Element}
   * @constructor
   */
  const { sessionData, setSessionData } = useSession()

  const ProtectedRoute = ({
                            redirectPath = `/${LOGIN_PAGE_RESOURCE}`,
                            children
                          }) => {
    if (!sessionData) {
      toast.error('Only logged in users can access this page')
      return <Navigate to={redirectPath} replace />
    }
    return children
  }

  return (
    <div className="App container-fluid">
      <Toaster
        position="top-center"
        reverseOrder={false}
      />
      <div className="row">
        <div className="col-sm-12">
          <BrowserRouter>
            <Routes>
              <Route path="/"
                     element={<MainContainer sessionData={sessionData}
                                             setSessionData={setSessionData} />}>
                <Route index element={<Navigate to="login-page" />}>
                </Route>
                <Route path={EMULATIONS_PAGE_RESOURCE} index element={
                  <ProtectedRoute>
                    <Emulations sessionData={sessionData}
                                setSessionData={setSessionData}
                    />
                  </ProtectedRoute>}>
                </Route>
                <Route path={SIMULATIONS_PAGE_RESOURCE} index element={
                  <ProtectedRoute>
                    <Simulations sessionData={sessionData} setSessionData={setSessionData} />
                  </ProtectedRoute>}>
                </Route>
                <Route path={MONITORING_PAGE_RESOURCE} index element={
                  <ProtectedRoute>
                    <Monitoring sessionData={sessionData} setSessionData={setSessionData} />
                  </ProtectedRoute>}>
                </Route>
                <Route path={TRACES_PAGE_RESOURCE} index element={
                  <ProtectedRoute>
                    <Traces sessionData={sessionData} setSessionData={setSessionData} />
                  </ProtectedRoute>
                }>
                </Route>
                <Route path={EMULATION_STATISTICS_PAGE_RESOURCE} index element={
                  <ProtectedRoute>
                    <EmulationStatistics sessionData={sessionData} setSessionData={setSessionData} />
                  </ProtectedRoute>
                }>
                </Route>
                <Route path={SYSTEM_MODELS_PAGE_RESOURCE} index element={
                  <ProtectedRoute>
                    <SystemModels sessionData={sessionData} setSessionData={setSessionData} />
                  </ProtectedRoute>
                }>
                </Route>
                <Route path={POLICY_EXAMINATION_PAGE_RESOURCE} index element={
                  <ProtectedRoute>
                    <PolicyExamination sessionData={sessionData} setSessionData={setSessionData} />
                  </ProtectedRoute>
                }>
                </Route>
                <Route path={IMAGES_PAGE_RESOURCE} index element={
                  <ProtectedRoute>
                    <ContainerImages sessionData={sessionData} setSessionData={setSessionData} />
                  </ProtectedRoute>
                }>
                </Route>
                <Route path={TRAINING_PAGE_RESOURCE} index element={
                  <ProtectedRoute>
                    <TrainingResults sessionData={sessionData} setSessionData={setSessionData} />
                  </ProtectedRoute>
                }>
                </Route>
                <Route path={POLICIES_PAGE_RESOURCE} index element={
                  <ProtectedRoute>
                    <Policies sessionData={sessionData} setSessionData={setSessionData} />
                  </ProtectedRoute>
                }>
                </Route>
                <Route path={JOBS_PAGE_RESOURCE} index element={
                  <ProtectedRoute>
                    <Jobs sessionData={sessionData} setSessionData={setSessionData} />
                  </ProtectedRoute>
                }>
                </Route>
                <Route path={SDN_CONTROLLERS_PAGE_RESOURCE} index element={
                  <ProtectedRoute>
                    <SDNControllers sessionData={sessionData} setSessionData={setSessionData} />
                  </ProtectedRoute>
                }>
                </Route>
                <Route path={CONTROL_PLANE_PAGE_RESOURCE} index element={
                  <ProtectedRoute>
                    <ControlPlane sessionData={sessionData} setSessionData={setSessionData} />
                  </ProtectedRoute>
                }>
                </Route>
                <Route path={CONTAINER_TERMINAL_PAGE_RESOURCE} index element={
                  <ProtectedRoute>
                    <ContainerTerminal sessionData={sessionData} setSessionData={setSessionData} />
                  </ProtectedRoute>
                }>
                </Route>
                <Route path={ABOUT_PAGE_RESOURCE} index element={<About />}>
                </Route>
                <Route path={DOWNLOADS_PAGE_RESOURCE} index
                       element={<Downloads sessionData={sessionData}
                                           setSessionData={setSessionData} />}>
                </Route>
                <Route path={LOGIN_PAGE_RESOURCE} index element={<Login setSessionData={setSessionData}
                                                                        sessionData={sessionData} />}>
                </Route>
                <Route path={REGISTER_PAGE_RESOURCE} index element={<Register />}>
                </Route>
                <Route path={USER_ADMIN_PAGE_RESOURCE} index element={
                  <ProtectedRoute>
                    <UserAdmin sessionData={sessionData} setSessionData={setSessionData} />
                  </ProtectedRoute>
                }>
                </Route>
                <Route path={SYSTEM_ADMIN_PAGE_RESOURCE} index element={
                  <ProtectedRoute>
                    <SystemAdmin sessionData={sessionData} setSessionData={setSessionData} />
                  </ProtectedRoute>
                }>
                </Route>
                <Route path={LOGS_ADMIN_PAGE_RESOURCE} index element={
                  <ProtectedRoute>
                    <LogsAdmin sessionData={sessionData} setSessionData={setSessionData} />
                  </ProtectedRoute>
                }>
                </Route>
                <Route path={SERVER_CLUSTER_PAGE_RESOURCE} index element={
                  <ProtectedRoute>
                    <ServerCluster sessionData={sessionData} setSessionData={setSessionData} />
                  </ProtectedRoute>
                }>
                </Route>
                <Route path={CREATE_EMULATION_PAGE_RESOURCE} index element={
                  <ProtectedRoute>
                    <CreateEmulation sessionData={sessionData} setSessionData={setSessionData} />
                  </ProtectedRoute>
                }>
                </Route>
                <Route path={RECOVERY_AI_PAGE_RESOURCE} index element={
                  <ProtectedRoute>
                    <RecoveryAI sessionData={sessionData} setSessionData={setSessionData} />
                  </ProtectedRoute>
                }>
                </Route>
                <Route path="*" element={<NotFound />} />
              </Route>
            </Routes>
          </BrowserRouter>
        </div>
      </div>
    </div>
  )
}

export default App
