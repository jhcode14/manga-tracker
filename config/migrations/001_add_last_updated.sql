DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 
        FROM information_schema.columns 
        WHERE table_name='manga' AND column_name='last_updated'
    ) THEN
        ALTER TABLE manga ADD COLUMN last_updated INT;
        
        UPDATE manga
        SET last_updated = 0;
    END IF;
END $$;
