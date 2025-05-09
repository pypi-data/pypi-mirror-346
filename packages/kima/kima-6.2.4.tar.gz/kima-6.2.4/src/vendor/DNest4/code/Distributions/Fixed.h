#pragma once

// DNest4/code
#include "ContinuousDistribution.h"
#include "../RNG.h"

namespace DNest4
{

/*
* Not a real distribution, just a fixed parameter
*/
class Fixed:public ContinuousDistribution
{
    public:
        double val;

        Fixed(double val=0.0);

        double cdf(double x) const override;
        double cdf_inverse(double p) const override;
        double log_pdf(double x) const override;
        // ostream representation of Fixed class
        virtual std::ostream& print(std::ostream& out) const override
        {
            out << "Fixed(" << val << ")";
            return out;
        }
        // this special class reimplements perturb to save some work
        double perturb(double& x, RNG& rng) const;
};

} // namespace DNest4

