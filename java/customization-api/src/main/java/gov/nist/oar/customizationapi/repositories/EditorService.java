package gov.nist.oar.customizationapi.repositories;

import org.bson.Document;

import gov.nist.oar.customizationapi.exceptions.CustomizationException;
import gov.nist.oar.customizationapi.exceptions.InvalidInputException;

public interface EditorService {
	
	/**
	 * Updates record with provided input changes.
	 * 
	 * @param param    JSON string
	 * @param recordid string ediid/unique record id
	 * @return Complete record with updated fields
	 * @throws CustomizationException if there is an issue update record in data
	 *                                base or getting record from backend for the
	 *                                first time to put chnages in cache, it would
	 *                                throw internal service error
	 * @throws InvalidInputException  If input parameters are not valid and fail
	 *                                JSON validation tests, this exception is
	 *                                thrown
	 */
	public Document patchRecord(String param, String recordid) throws CustomizationException, InvalidInputException;

	/**
	 * Returns the complete record in JSON format which can be used to edit.
	 * 
	 * @param recordid string ediid/unique record id
	 * @return Document a complete JSON data
	 * @throws CustomizationException Throws exception if there is issue while
	 *                                accessing data
	 */
	public Document getRecord(String recordid) throws CustomizationException;

	
	/**
	 * Delete changes made for this record from the database
	 * 
	 * @param recordid string ediid/unique record id
	 * @return boolean successfully deleted changes
	 * @throws CustomizationException Exception thrown if any error is thrown while
	 *                                deleting record from backend
	 */
	public Document deleteRecordChanges(String recordid) throws CustomizationException;
}
