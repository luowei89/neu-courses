ALTER TABLE `AP_DATA`.`PUBLICATION` 
ADD COLUMN `CITES` INT NULL DEFAULT 0 AFTER `VENUE`,
ADD COLUMN `CITED` INT NULL DEFAULT 0 AFTER `CITES`;

UPDATE PUBLICATION SET CITES = 
(SELECT COUNT(*) FROM CITATION 
WHERE CITATION.PUB_ID = PUBLICATION.PUB_ID);

UPDATE PUBLICATION SET CITED = 
(SELECT COUNT(*) FROM CITATION 
WHERE CITATION.REF_ID = PUBLICATION.PUB_ID);

ALTER TABLE `AP_DATA`.`AUTHOR` 
ADD COLUMN `PUBS` INT NULL DEFAULT 0 AFTER `NAME`;

UPDATE AUTHOR SET PUBS = 
(SELECT COUNT(*) FROM AUTHOR_PUB 
WHERE AUTHOR.AUTHOR_ID = AUTHOR_PUB.AUTHOR_ID);

DELETE FROM AUTHOR_PUB WHERE AUTHOR_ID IN (1444444,1606682);# '' AND 'STAFF'
DELETE FROM AUTHOR WHERE AUTHOR_ID IN (1444444,1606682);