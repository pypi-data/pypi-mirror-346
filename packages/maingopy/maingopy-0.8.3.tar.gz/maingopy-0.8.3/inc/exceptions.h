/**********************************************************************************
 * Copyright (c) 2019 Process Systems Engineering (AVT.SVT), RWTH Aachen University
 *
 * This program and the accompanying materials are made available under the
 * terms of the Eclipse Public License 2.0 which is available at
 * http://www.eclipse.org/legal/epl-2.0.
 *
 * SPDX-License-Identifier: EPL-2.0
 *
 * @file exceptions.h
 *
 * @brief File declaring the MAiNGO exception class.
 *
 **********************************************************************************/

#pragma once

#include "babNode.h"

#include <exception>
#include <sstream>
#include <string>
#include <typeinfo>


namespace maingo {


/**
* @class MAiNGOException
* @brief This class defines the exceptions thrown by MAiNGO
*
* The class contains different constructors. The first parameter is always the error message.
* For debugging, the error message will also contain the file name and line number
* Additionally, the constructor can take an exception as second argument.
* If done so, the type of the exception object and its what() will be saved in the error message as well.
*
*/
class MAiNGOException: public std::exception {

  private:
    std::string _msg{""}; /*!< string holding the exception message */
    MAiNGOException();

  public:
    /**
	* @brief Constructor used for forwarding
	*
	* @param[in] arg is a string holding an error message
	*/
    explicit MAiNGOException(const std::string& arg):
        MAiNGOException(arg, nullptr, nullptr)
    {
    }

    /**
	* @brief Constructor used for forwarding
	*
	* @param[in] arg is a string holding an error message
	* @param[in] node holds the current BabNode
	*/
    MAiNGOException(const std::string& arg, const babBase::BabNode& node):
        MAiNGOException(arg, nullptr, &node)
    {
    }

    /**
	* @brief Constructor used for forwarding
	*
	* @param[in] arg is a string holding an error message
	* @param[in] e holds the exception
	*/
    MAiNGOException(const std::string& arg, const std::exception& e):
        MAiNGOException(arg, &e, nullptr)
    {
    }

    /**
	* @brief Constructor used for forwarding
	*
	* @param[in] arg is a string holding an error message
	* @param[in] e holds the exception
	* @param[in] node holds the current BabNode
	*/
    MAiNGOException(const std::string& arg, const std::exception& e, const babBase::BabNode& node):
        MAiNGOException(arg, &e, &node)
    {
    }

    /**
	* @brief Constructor used printing a MAiNGO Exception
	*
	* @param[in] arg is a string holding an error message
	* @param[in] e holds the exception
	* @param[in] node holds the current BabNode
	*/
    MAiNGOException(const std::string& arg, const std::exception* e, const babBase::BabNode* node)
    {
        std::ostringstream message;
        if (e) {
            if (typeid(*e).name() != typeid(*this).name()) {
                message << "  Original std::exception: " << typeid(*e).name() << ": " << std::endl
                        << "   ";
            }
            message << e->what() << std::endl;
        }
        message << arg;
        if (node) {
            std::vector<double> lowerVarBounds(node->get_lower_bounds()), upperVarBounds(node->get_upper_bounds());
            message << std::endl
                    << "  Exception was thrown while processing node no. " << node->get_ID() << ":";
            for (unsigned int i = 0; i < lowerVarBounds.size(); i++) {
                message << std::endl
                        << "    x(" << i << "): " << std::setprecision(16) << lowerVarBounds[i] << ":" << upperVarBounds[i];
            }
        }
        _msg = message.str();
    }


    /**
    * @brief Function to return the error message
	*
    * @return Error message.
    */
    const char* what() const noexcept
    {
        return _msg.c_str();
    }
};


#ifdef HAVE_MAiNGO_MPI
/**
* @class MAiNGOMpiException
* @brief This class defines the exceptions thrown by MAiNGO when using MPI
*
* In addition to the MAiNGOException class, it contains an enum to distinguish which process the exception came from.
*/
class MAiNGOMpiException: public MAiNGOException {

  public:
    /**
	* @enum TYPE
	* @brief Enum for Branch and Bound exception handling
	*/
    enum TYPE {
        MPI_ME = 1, /*!< Exception thrown by the process the exception is thrown on */
        MPI_OTHER   /*!< Exception thrown by other process */
    };

    /**
	* @brief Constructor used for forwarding
	*
	* @param[in] ierr is the process type
	*/
    explicit MAiNGOMpiException(TYPE ierr):
        MAiNGOMpiException("", nullptr, nullptr, ierr)
    {
    }

    /**
	* @brief Constructor used for forwarding
	*
	* @param[in] arg is a string holding an error message
	* @param[in] ierr is the process type
	*/
    MAiNGOMpiException(const std::string& arg, TYPE ierr):
        MAiNGOMpiException(arg, nullptr, nullptr, ierr)
    {
    }

    /**
	* @brief Constructor used for forwarding
	*
	* @param[in] arg is a string holding an error message
	* @param[in] node holds the current BabNode
	* @param[in] ierr is the process type
	*/
    MAiNGOMpiException(const std::string& arg, const babBase::BabNode& node, TYPE ierr):
        MAiNGOMpiException(arg, nullptr, &node, ierr)
    {
    }

    /**
	* @brief Constructor used for forwarding
	*
	* @param[in] arg is a string holding an error message
	* @param[in] e holds the exception
	* @param[in] ierr is the process type
	*/
    MAiNGOMpiException(const std::string& arg, const std::exception& e, TYPE ierr):
        MAiNGOMpiException(arg, &e, nullptr, ierr)
    {
    }

    /**
	* @brief Constructor used for forwarding
	*
	* @param[in] arg is a string holding an error message
	* @param[in] e holds the exception
	* @param[in] node holds the current BabNode
	* @param[in] ierr is the process type
	*/
    MAiNGOMpiException(const std::string& arg, const std::exception& e, const babBase::BabNode& node, TYPE ierr):
        MAiNGOMpiException(arg, &e, &node, ierr)
    {
    }

    /**
	* @brief Constructor used for forwarding to MAiNGOException
	*
	* @param[in] e holds the exception
	* @param[in] ierr is the process type
	*/
    MAiNGOMpiException(MAiNGOException& e, TYPE ierr):
        MAiNGOException(e), _ierr(ierr)
    {
    }

    /**
	* @brief Constructor used for forwarding to MAiNGOException
	*
	* @param[in] arg is a string holding an error message
	* @param[in] e holds the exception
	* @param[in] node holds the current BabNode
	* @param[in] ierr is the process type
	*/
    MAiNGOMpiException(const std::string& arg, const std::exception* e, const babBase::BabNode* node, TYPE ierr):
        MAiNGOException(arg, e, node), _ierr(ierr)
    {
    }

    /**
	* @brief Function for returning the MPI error type
	*/
    int ierr() { return _ierr; }


  private:
    TYPE _ierr; /*!< MPI error type */
};
#endif

}    // end namespace maingo