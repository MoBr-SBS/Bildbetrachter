QToolBar#MainToolbar {
    background-color: #2b2b2b;
    border: none;
    border-bottom: 1px solid #3a3a3a;
    spacing: 6px;
    padding: 6px 8px;
}

QToolBar#MainToolbar::separator {
    width: 10px;
    background: transparent;
}

QToolBar#MainToolbar QToolButton {
    background-color: #343434;
    color: #f2f2f2;
    border: 1px solid #474747;
    border-radius: 5px;
    padding: 5px 12px;
    min-height: 26px;
    font-weight: 600;
}

QToolBar#MainToolbar QToolButton:hover {
    background-color: #404040;
    border: 1px solid #5e5e5e;
}

QToolBar#MainToolbar QToolButton:pressed {
    background-color: #262626;
    border: 1px solid #6a6a6a;
}

QToolBar#MainToolbar QToolButton:disabled {
    color: #8c8c8c;
    background-color: #303030;
    border: 1px solid #404040;
}
