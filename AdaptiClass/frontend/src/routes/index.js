import React from "react"
import PathConstants from "./pathConstants"

const HomeContent = React.lazy(() => import("../pages/Home"))
const CourseContent = React.lazy(() => import("../pages/Courses"))
const FeedbackContent = React.lazy(() => import("../pages/Feedback"))
const SettingsContent = React.lazy(() => import("../pages/Settings"))

const routes = [
    { path: PathConstants.HOME, element: <HomeContent /> },
    { path: PathConstants.COURSES, element: <CourseContent /> },
    { path: PathConstants.FEEDBACK, element: <FeedbackContent /> },
    { path: PathConstants.SETTINGS, element: <SettingsContent /> },
]
export default routes