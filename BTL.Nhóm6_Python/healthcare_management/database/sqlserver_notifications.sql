IF OBJECT_ID('dbo.UserSettings', 'U') IS NULL
BEGIN
    CREATE TABLE dbo.UserSettings (
        user_id INT PRIMARY KEY,
        gender NVARCHAR(10) NULL DEFAULT N'Nam',
        dob DATE NULL,
        address NVARCHAR(255) NULL DEFAULT N'',
        avatar_path NVARCHAR(255) NULL DEFAULT N'',
        notify_new_appointment BIT NOT NULL DEFAULT 1,
        notify_reminder BIT NOT NULL DEFAULT 1,
        notify_system BIT NOT NULL DEFAULT 1,
        theme_mode NVARCHAR(20) NULL DEFAULT N'Sáng',
        font_size NVARCHAR(20) NULL DEFAULT N'Trung bình',
        display_density NVARCHAR(20) NULL DEFAULT N'Thoải mái',
        language NVARCHAR(20) NULL DEFAULT N'Tiếng Việt',
        backup_mode NVARCHAR(20) NULL DEFAULT N'cloud',
        last_backup_at DATETIME2 NULL,
        last_sync_at DATETIME2 NULL,
        updated_at DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME(),
        CONSTRAINT FK_UserSettings_Users FOREIGN KEY (user_id) REFERENCES dbo.Users(user_id)
    );
END;

IF OBJECT_ID('dbo.Notifications', 'U') IS NULL
BEGIN
    CREATE TABLE dbo.Notifications (
        notification_id INT IDENTITY(1,1) PRIMARY KEY,
        user_id INT NOT NULL,
        title NVARCHAR(150) NOT NULL,
        content NVARCHAR(500) NULL,
        type NVARCHAR(50) NOT NULL DEFAULT N'system',
        target_page NVARCHAR(50) NOT NULL DEFAULT N'dashboard',
        target_id INT NULL,
        is_read BIT NOT NULL DEFAULT 0,
        created_at DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME(),
        read_at DATETIME2 NULL,
        CONSTRAINT FK_Notifications_Users FOREIGN KEY (user_id) REFERENCES dbo.Users(user_id),
        CONSTRAINT CK_Notifications_TargetPage CHECK (target_page IN ('schedule','patient_profile','prescriptions','dashboard','settings'))
    );
END;

IF NOT EXISTS (
    SELECT 1
    FROM sys.indexes
    WHERE name = 'IX_Notifications_User_Read'
      AND object_id = OBJECT_ID('dbo.Notifications')
)
BEGIN
    CREATE INDEX IX_Notifications_User_Read
    ON dbo.Notifications(user_id, is_read, created_at DESC);
END;
